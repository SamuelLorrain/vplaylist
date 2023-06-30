"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { authenticationToken } from '@/contexts/recoilState';
import { useRecoilValue } from 'recoil';

const RouteGuard = ({children}: {children: React.ReactNode}) => {
    const router = useRouter();
    const token = useRecoilValue(authenticationToken);

    if (token == null || token == '') {
        router.push('/');

        return <></>;
    }

    return <>
      {children}
    </>;
}

export default RouteGuard;
