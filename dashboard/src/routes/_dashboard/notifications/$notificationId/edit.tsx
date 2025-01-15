import { createFileRoute, useNavigate } from '@tanstack/react-router'
import {
  MutationDialog,
  useRouterNotificationContext,
} from '@marzneshin/modules/notifications'

const NotificationEdit = () => {
  const value = useRouterNotificationContext()
  const navigate = useNavigate({ from: '/notifications/$notificationId/edit' })

  return (
    value && (
      <MutationDialog
        entity={value.notification}
        onClose={() => navigate({ to: '/notifications' })}
      />
    )
  )
}

export const Route = createFileRoute(
  '/_dashboard/notifications/$notificationId/edit',
)({
  component: NotificationEdit,
})
