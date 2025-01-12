import * as React from 'react'

interface ToastDescriptionProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

export function ToastDescription({ children, ...props }: ToastDescriptionProps) {
  return (
    <div {...props} className="text-sm opacity-90">
      {children}
    </div>
  )
}
