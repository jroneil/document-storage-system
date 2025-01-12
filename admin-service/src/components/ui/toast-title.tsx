import * as React from 'react'

interface ToastTitleProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

export function ToastTitle({ children, ...props }: ToastTitleProps) {
  return (
    <div {...props} className="text-sm font-semibold">
      {children}
    </div>
  )
}
