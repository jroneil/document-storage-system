"use client";

import React from "react";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Input } from "./input";

type DatePickerProps = {
  /** Currently selected date */
  selected: Date | null;
  /** Callback when date changes */
  onChange: (date: Date | null) => void;
  /** Placeholder text for the input */
  placeholderText?: string;
  /** Custom input component */
  customInput?: React.ReactElement;
  /** Date format string */
  dateFormat?: string;
  /** Show year dropdown */
  showYearDropdown?: boolean;
  /** Show month dropdown */
  showMonthDropdown?: boolean;
  /** Dropdown mode */
  dropdownMode?: "scroll" | "select";
};

export function DatePickerComponent({
  selected,
  onChange,
  placeholderText,
  customInput = <Input />,
  dateFormat = "MM/dd/yyyy",
  showYearDropdown = true,
  showMonthDropdown = true,
  dropdownMode = "select",
  ...props
}: DatePickerProps) {
  const DatePicker = ReactDatePicker as any;
  
  return (
    <DatePicker
      selected={selected}
      onChange={onChange}
      placeholderText={placeholderText}
      customInput={customInput}
      dateFormat={dateFormat}
      showYearDropdown={showYearDropdown}
      showMonthDropdown={showMonthDropdown}
      dropdownMode={dropdownMode}
      {...props}
    />
  );
}
