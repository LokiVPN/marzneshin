import { Page, Loading } from '@marzneshin/common/components'
import { NotificationsTable } from '@marzneshin/modules/notifications'
import { createLazyFileRoute, Outlet } from '@tanstack/react-router'
import { type FC, Suspense } from 'react'
import { useTranslation } from 'react-i18next'

export const NotificationsPage: FC = () => {
  const { t } = useTranslation()

  return (
    <Page title={t('notifications')}>
      <NotificationsTable />
      <Suspense fallback={<Loading />}>
        <Outlet />
      </Suspense>
    </Page>
  )
}

export const Route = createLazyFileRoute('/_dashboard/notifications')({
  component: () => <NotificationsPage />,
})
