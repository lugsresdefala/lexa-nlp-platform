-- LEXA Supabase Security Fixes
-- Addresses the security warnings from the database linter

-- Fix function search_path mutability for security
-- These functions need to have search_path set to prevent SQL injection

-- Fix deduct_credits_for_analysis function
CREATE OR REPLACE FUNCTION public.deduct_credits_for_analysis(
    user_id_param UUID,
    credits_to_deduct INTEGER
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    current_credits INTEGER;
BEGIN
    -- Get current user credits
    SELECT credits INTO current_credits
    FROM auth.users
    WHERE id = user_id_param;
    
    -- Check if user has enough credits
    IF current_credits >= credits_to_deduct THEN
        -- Deduct credits
        UPDATE auth.users
        SET credits = credits - credits_to_deduct
        WHERE id = user_id_param;
        
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$;

-- Fix get_user_type function
CREATE OR REPLACE FUNCTION public.get_user_type(user_id_param UUID)
RETURNS TEXT
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    user_plan TEXT;
BEGIN
    SELECT plan INTO user_plan
    FROM auth.users
    WHERE id = user_id_param;
    
    RETURN COALESCE(user_plan, 'free');
END;
$$;

-- Fix get_user_credits function
CREATE OR REPLACE FUNCTION public.get_user_credits(user_id_param UUID)
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    user_credits INTEGER;
BEGIN
    SELECT credits INTO user_credits
    FROM auth.users
    WHERE id = user_id_param;
    
    RETURN COALESCE(user_credits, 0);
END;
$$;

-- Enable Row Level Security on custom tables
ALTER TABLE IF EXISTS users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS texts ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for users table
DROP POLICY IF EXISTS "Users can view own data" ON users;
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id::uuid);

DROP POLICY IF EXISTS "Users can update own data" ON users;
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id::uuid);

-- Create RLS policies for texts table
DROP POLICY IF EXISTS "Users can view own texts" ON texts;
CREATE POLICY "Users can view own texts" ON texts
    FOR SELECT USING (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Users can insert own texts" ON texts;
CREATE POLICY "Users can insert own texts" ON texts
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT, INSERT, UPDATE ON users TO authenticated;
GRANT SELECT, INSERT ON texts TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_type(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_credits(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION deduct_credits_for_analysis(UUID, INTEGER) TO authenticated;