'use client'

import { useEffect, useRef } from 'react'

interface PopupProps {
  children: React.ReactNode
  onClose: () => void
}

export default function Popup({ children, onClose }: PopupProps) {
  const popupRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
        onClose()
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [onClose])

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div ref={popupRef} className="bg-white rounded-lg shadow-lg p-6 max-w-2xl w-full">
        {children}
      </div>
    </div>
  )
}
