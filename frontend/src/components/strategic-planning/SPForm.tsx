import { ReactNode } from "react";
import { Formik, Form, FormikConfig, FormikValues, useField } from "formik";
import { CircularProgress } from "@mui/material";
import { TextField as MuiTextField, TextFieldProps as MuiTextFieldProps } from "@mui/material";
import { Select, MenuItem, FormControl, InputLabel, SelectProps, Checkbox, FormControlLabel, Switch, FormControlLabelProps } from "@mui/material";
import { LocalizationProvider, DatePicker, DatePickerProps } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs, { Dayjs } from "dayjs";

interface SPFormProps<T extends FormikValues> extends Omit<FormikConfig<T>, 'component'> {
  children: ReactNode;
  loading?: boolean;
}

export function SPForm<T extends FormikValues>({ children, loading, ...formikProps }: SPFormProps<T>) {
  return (
    <Formik {...formikProps}>
      {(props) => (
        <Form>
          {typeof children === 'function' ? children(props) : children}
          {loading && (
            <div className="flex justify-center items-center py-4">
              <CircularProgress size={24} />
            </div>
          )}
        </Form>
      )}
    </Formik>
  );
}

interface SPTextFieldProps extends Omit<MuiTextFieldProps, 'name'> {
  name: string;
  label?: string;
  required?: boolean;
}

export function SPTextField({ name, label, required, ...props }: SPTextFieldProps) {
  const [field, meta] = useField(name);

  return (
    <MuiTextField
      {...field}
      {...props}
      label={label}
      required={required}
      error={Boolean(meta.touched && meta.error)}
      helperText={meta.touched && meta.error}
      fullWidth
      size="small"
    />
  );
}

interface SPSelectProps extends Omit<SelectProps<string>, 'name' | 'label'> {
  name: string;
  label?: string;
  options: { value: string; label: string }[];
  required?: boolean;
}

export function SPSelect({ name, label, options, required, ...props }: SPSelectProps) {
  const [field, meta] = useField(name);

  return (
    <FormControl fullWidth size="small" error={Boolean(meta.touched && meta.error)}>
      {label && <InputLabel required={required}>{label}</InputLabel>}
      <Select {...field} {...props} label={label}>
        {options.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </Select>
      {meta.touched && meta.error && <span className="text-error text-xs mt-1">{meta.error}</span>}
    </FormControl>
  );
}

interface SPCheckboxProps {
  name: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
}

export function SPCheckbox({ name, label, required, disabled }: SPCheckboxProps) {
  const [field, meta] = useField({ name, type: 'checkbox' });

  return (
    <FormControlLabel
      control={<Checkbox {...field} disabled={disabled} color="primary" />}
      label={label}
      required={required}
      error={Boolean(meta.touched && meta.error)}
      helperText={meta.touched && meta.error}
    />
  );
}

interface SPSwitchProps extends Omit<FormControlLabelProps, 'control'> {
  name: string;
  label?: string;
  disabled?: boolean;
}

export function SPSwitch({ name, label, disabled, ...props }: SPSwitchProps) {
  const [field] = useField({ name, type: 'checkbox' });

  return (
    <FormControlLabel
      {...props}
      control={<Switch {...field} disabled={disabled} />}
      label={label}
    />
  );
}

interface SPDatePickerProps extends Omit<DatePickerProps<Dayjs>, 'value' | 'onChange'> {
  name: string;
  label?: string;
  required?: boolean;
}

export function SPDatePicker({ name, label, required, ...props }: SPDatePickerProps) {
  const [field, meta, helpers] = useField(name);

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker
        {...props}
        label={label}
        value={field.value ? dayjs(field.value) : null}
        onChange={(date) => helpers.setValue(date ? date.toISOString() : null)}
        slotProps={{
          textField: {
            fullWidth: true,
            size: 'small',
            error: Boolean(meta.touched && meta.error),
            helperText: meta.touched && meta.error,
            required,
          },
        }}
      />
    </LocalizationProvider>
  );
}

interface SPTextAreaProps extends Omit<MuiTextFieldProps, 'name'> {
  name: string;
  label?: string;
  required?: boolean;
  rows?: number;
}

export function SPTextArea({ name, label, required, rows = 4, ...props }: SPTextAreaProps) {
  const [field, meta] = useField(name);

  return (
    <MuiTextField
      {...field}
      {...props}
      label={label}
      required={required}
      multiline
      rows={rows}
      error={Boolean(meta.touched && meta.error)}
      helperText={meta.touched && meta.error}
      fullWidth
      size="small"
    />
  );
}

// Validation helpers using Yup
import * as yup from 'yup';

export const SPValidation = {
  required: (message = 'Field ini wajib diisi') => yup.string().required(message),
  email: (message = 'Email tidak valid') => yup.string().email(message),
  minLength: (min: number, message?: string) =>
    yup.string().min(min, message || `Minimal ${min} karakter`),
  maxLength: (max: number, message?: string) =>
    yup.string().max(max, message || `Maksimal ${max} karakter`),
  number: (message = 'Harus berupa angka') => yup.number().typeError(message),
  min: (min: number, message?: string) =>
    yup.number().min(min, message || `Minimal ${min}`),
  max: (max: number, message?: string) =>
    yup.number().max(max, message || `Maksimal ${max}`),
  phone: (message = 'Nomor telepon tidak valid') =>
    yup.string().matches(/^[0-9+\-\s()]*$/, message),
  url: (message = 'URL tidak valid') => yup.string().url(message),
  date: (message = 'Tanggal tidak valid') => yup.date().typeError(message),
};

export default SPForm;