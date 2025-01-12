import { NextResponse } from 'next/server'
import { apiClient } from '@/lib/apiClient'

export async function GET(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params
    const response = await apiClient.get(`/metadata/user-preferences/${userId}`)
    return NextResponse.json(response.data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch user preferences' },
      { status: 500 }
    )
  }
}

export async function POST(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params
    const body = await request.json()
    const response = await apiClient.post(
      `/metadata/user-preferences/${userId}/save-search`,
      body
    )
    return NextResponse.json(response.data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to save search' },
      { status: 500 }
    )
  }
}

export async function PUT(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params
    const body = await request.json()
    const response = await apiClient.put(
      `/metadata/user-preferences/${userId}/columns`,
      body
    )
    return NextResponse.json(response.data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update columns' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { userId: string; searchName: string } }
) {
  try {
    const { userId, searchName } = params
    const response = await apiClient.delete(
      `/metadata/user-preferences/${userId}/search/${searchName}`
    )
    return NextResponse.json(response.data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to delete search' },
      { status: 500 }
    )
  }
}
