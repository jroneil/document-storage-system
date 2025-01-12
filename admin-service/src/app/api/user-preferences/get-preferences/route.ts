import { NextResponse } from 'next/server'
import { apiClient } from '@/lib/apiClient'

export async function GET() {
  try {
    const response = await apiClient.get('/api/user-preferences')
    return NextResponse.json(response.data)
  } catch (error: any) {
    return NextResponse.json(
      { error: error.response?.data?.message || error.message },
      { status: error.response?.status || 500 }
    )
  }
}
