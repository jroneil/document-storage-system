import { NextResponse } from 'next/server'
import { apiClient } from '@/lib/apiClient'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const response = await apiClient.post('/api/user-preferences/save-search', body)
    return NextResponse.json(response.data)
  } catch (error: any) {
    return NextResponse.json(
      { error: error.response?.data?.message || error.message },
      { status: error.response?.status || 500 }
    )
  }
}
