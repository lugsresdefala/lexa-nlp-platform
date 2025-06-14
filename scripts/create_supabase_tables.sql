-- LEXA Database Schema for Supabase
-- Creates the necessary tables and functions for the LEXA application

-- Create users table to extend auth.users
CREATE TABLE IF NOT EXISTS public.users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT NOT NULL,
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'premium', 'enterprise')),
    char_usage INTEGER DEFAULT 0,
    credits INTEGER DEFAULT 1000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create texts table for storing analyzed texts
CREATE TABLE IF NOT EXISTS public.texts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    language TEXT DEFAULT 'pt',
    domain TEXT DEFAULT 'Acadêmico',
    analysis_results JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create analysis_sessions table for tracking usage
CREATE TABLE IF NOT EXISTS public.analysis_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    text_length INTEGER NOT NULL,
    analysis_type TEXT NOT NULL,
    credits_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_texts_user_id ON public.texts(user_id);
CREATE INDEX IF NOT EXISTS idx_texts_created_at ON public.texts(created_at);
CREATE INDEX IF NOT EXISTS idx_analysis_sessions_user_id ON public.analysis_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_analysis_sessions_created_at ON public.analysis_sessions(created_at);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to handle new user registration
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.users (id, email, plan, char_usage, credits)
    VALUES (NEW.id, NEW.email, 'free', 0, 1000);
    RETURN NEW;
END;
$$;

-- Create trigger for new user registration
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Create function to check user quota
CREATE OR REPLACE FUNCTION public.check_user_quota(
    user_id_param UUID,
    text_length INTEGER
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    user_plan TEXT;
    current_usage INTEGER;
    monthly_limit INTEGER;
BEGIN
    -- Get user plan and current usage
    SELECT plan, char_usage INTO user_plan, current_usage
    FROM public.users
    WHERE id = user_id_param;
    
    -- Set limits based on plan
    CASE user_plan
        WHEN 'free' THEN monthly_limit := 10000;
        WHEN 'premium' THEN monthly_limit := 100000;
        WHEN 'enterprise' THEN monthly_limit := 1000000;
        ELSE monthly_limit := 10000;
    END CASE;
    
    -- Check if adding this text would exceed the limit
    IF (current_usage + text_length) <= monthly_limit THEN
        -- Update usage
        UPDATE public.users
        SET char_usage = char_usage + text_length
        WHERE id = user_id_param;
        
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$;

-- Enable Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.texts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analysis_sessions ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- RLS Policies for texts table
CREATE POLICY "Users can view own texts" ON public.texts
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own texts" ON public.texts
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

-- RLS Policies for analysis_sessions table
CREATE POLICY "Users can view own sessions" ON public.analysis_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" ON public.analysis_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Grant permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON public.users TO authenticated;
GRANT ALL ON public.texts TO authenticated;
GRANT ALL ON public.analysis_sessions TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;