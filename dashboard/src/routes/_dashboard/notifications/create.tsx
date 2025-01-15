import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { MutationDialog } from '@marzneshin/modules/notifications'

const NotificationCreate = () => {
  const navigate = useNavigate({ from: '/notifications/create' })
  return (
    <MutationDialog
      entity={null}
      onClose={() => navigate({ to: '/notifications' })}
    />
  )
}

export const Route = createFileRoute('/_dashboard/notifications/create')({
  component: NotificationCreate,
})
