# LEXA Supabase Setup Guide

## Database Connection Setup

To connect your LEXA application to Supabase, follow these steps:

### 1. Get Your Supabase Database URL

1. Go to your Supabase dashboard: https://supabase.com/dashboard/projects
2. Select your project (or create a new one)
3. Go to Settings → Database
4. Find "Connection string" and select "URI"
5. Copy the connection string that looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.criejhnwhltrkbctiixh.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual database password

### 2. Set the DATABASE_URL Secret

The system will prompt you for the DATABASE_URL secret. Provide the complete connection string from step 1.

### 3. Run Database Setup Scripts

Once connected, you need to create the database tables and security policies. Run these SQL scripts in your Supabase SQL editor:

#### A. Create Tables (run first):
```sql
-- Copy and paste the contents of scripts/create_supabase_tables.sql
```

#### B. Apply Security Fixes (run second):
```sql
-- Copy and paste the contents of scripts/supabase_security_fixes.sql
```

### 4. Security Recommendations

Based on your database linting report, implement these security measures:

1. **Function Security**: All database functions now use `SET search_path = public` to prevent SQL injection
2. **Row Level Security**: Enabled on all tables with proper policies
3. **Authentication**: Consider enabling leaked password protection in Supabase Auth settings
4. **OTP Expiry**: Reduce OTP expiry time to under 1 hour in Auth settings

### 5. Application Features

Once connected, your LEXA application will have:

- **User Authentication**: Secure registration and login
- **Usage Tracking**: Character limits based on subscription plans
- **Text Storage**: Persistent storage of analyzed texts
- **Analytics**: Usage statistics and analysis history

### 6. Plan Limits

- **Free**: 10,000 characters/month
- **Premium**: 100,000 characters/month  
- **Enterprise**: 1,000,000 characters/month

### 7. Monitoring

The application includes comprehensive error handling and will fall back to SQLite for development if Supabase is unavailable.

## Support

If you encounter issues:
1. Verify your DATABASE_URL format
2. Check Supabase project status
3. Ensure database scripts have been executed
4. Review the application logs for specific error messages
