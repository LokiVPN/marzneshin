import { type FC } from "react";
import { BooleanPill } from "@marzneshin/common/components";
import { useTranslation } from "react-i18next";
import type { TargetProp } from "@marzneshin/modules/notifications";



export const NotificationTargetSentAtPill: FC<TargetProp> = ({target}) => {
    const { t } = useTranslation();
    return (
        <BooleanPill
            active={target.sent_at !== null}
            activeLabel={t('sent')}
            inactiveLabel={t('not_yet')}
        />
    )
}
