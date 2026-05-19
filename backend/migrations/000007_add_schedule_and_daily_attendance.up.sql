CREATE TABLE IF NOT EXISTS trx_class_schedule (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    classroom_id uuid NOT NULL,
    teaching_assignment_id uuid NOT NULL,
    day_of_week smallint NOT NULL,
    start_time varchar(5) NOT NULL,
    end_time varchar(5) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT trx_class_schedule_pkey PRIMARY KEY (id),
    CONSTRAINT fk_class_schedule_classroom FOREIGN KEY (classroom_id) REFERENCES public.master_classroom(id) ON DELETE CASCADE,
    CONSTRAINT fk_class_schedule_teaching_assignment FOREIGN KEY (teaching_assignment_id) REFERENCES public.trx_teaching_assignment(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS trx_daily_attendance (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    classroom_id uuid NOT NULL,
    student_id uuid NOT NULL,
    date date NOT NULL,
    status varchar(20) NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT trx_daily_attendance_pkey PRIMARY KEY (id),
    CONSTRAINT fk_daily_attendance_classroom FOREIGN KEY (classroom_id) REFERENCES public.master_classroom(id) ON DELETE CASCADE,
    CONSTRAINT fk_daily_attendance_student FOREIGN KEY (student_id) REFERENCES public.master_student(id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_attendance ON trx_daily_attendance(classroom_id, student_id, date);
