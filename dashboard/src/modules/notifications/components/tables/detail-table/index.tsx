import { FC } from 'react'
import { NotificationType } from '../../../'
import { Table, TableBody, TableCell, TableHead, TableRow, DateTableRow } from '@marzneshin/common/components'
import { useTranslation } from 'react-i18next'
import MDEditor from '@uiw/react-md-editor';


interface NotificationDetailTableProps {
    notification: NotificationType
}


export const NotificationDetailTable: FC<NotificationDetailTableProps> = ({ notification }) => {
    const { t } = useTranslation()
    return (
        <Table>
            <TableBody>
                <TableRow >
                    <TableHead >
                        {t('label ')}
                    </TableHead>
                    <TableCell >
                        {notification.label}
                    </TableCell>
                </TableRow>
                <TableRow >
                    <TableHead >
                        {t('action')}
                    </TableHead>
                    <TableCell >
                        {notification.action}
                    </TableCell>
                </TableRow>
                <TableRow>
                    <TableHead >
                        {t('message')}
                    </TableHead>
                    <TableCell >
                        <MDEditor.Markdown source={notification.message} style={{ whiteSpace: 'pre-wrap' }} />
                    </TableCell>
                </TableRow>
                <DateTableRow
                    label={t("created_at")}
                    date={notification.created_at}
                    withTime
                />
                <DateTableRow
                    label={t("started_at")}
                    date={notification.started_at}
                    withTime
                />
                <DateTableRow
                    label={t("finished_at")}
                    date={notification.finished_at}
                    withTime
                />
            </TableBody>
        </Table>
    )
}
