"""Create User table

Revision ID: 3bdc4107cfc3
Revises: 
Create Date: 2024-09-12 15:54:42.637108

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3bdc4107cfc3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("auth.users.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("email", sa.String),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.execute(
        sa.DDL(
            """
            -- Set up Row Level Security (RLS)
            -- See https://supabase.com/docs/guides/auth/row-level-security for more details.
            alter table profiles
                enable row level security;

            create policy "Public profiles are viewable by everyone." on profiles
                for select using (true);

            create policy "Users can insert their own profile." on profiles
                for insert with check ((select auth.uid()) = id);

            create policy "Users can update own profile." on profiles
                for update using ((select auth.uid()) = id);

            -- This trigger automatically creates a profile entry when a new user signs up via Supabase Auth.
            -- See https://supabase.com/docs/guides/auth/managing-user-data#using-triggers for more details.
            create function public.handle_new_user()
            returns trigger
            set search_path = ''
            as $$
            begin
                insert into public.profiles (id, first_name, last_name, email, created_at, updated_at)
                values (new.id, new.raw_user_meta_data->>'first_name', new.raw_user_meta_data->>'last_name', new.email, new.created_at, new.updated_at);
                return new;
            end;
            $$ language plpgsql security definer;
            create trigger on_auth_user_created
                after insert on auth.users
                for each row execute procedure public.handle_new_user();
            """
        )
    )


def downgrade() -> None:
    op.drop_table("profiles")
    op.execute(
        sa.DDL(
            """
            drop trigger on_auth_user_created on auth.users;
            drop function public.handle_new_user();
            """
        )
    )
