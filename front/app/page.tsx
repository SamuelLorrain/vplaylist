"use client";

import { useCallback, useState, useEffect, FormEvent } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import { useRecoilState } from 'recoil';
import { authenticationToken } from '@/contexts/recoilState';

export default function LoginRegisterForm() {
    const [isRegister, setIsRegister] = useState(false);
    const router = useRouter();
    const [authenticationTokenValue, setAuthenticationToken] = useRecoilState(authenticationToken);

    useEffect(() => {
        if (authenticationTokenValue.length > 0) {
            router.push('/player');
        }
    }, [authenticationTokenValue]);

    const handleSubmit = useCallback((e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const form = new FormData(e.currentTarget)
        const username = String(form.get('username'));
        const password = String(form.get('password'));
        fetch(`${process.env.NEXT_PUBLIC_BACK_HOST}/${isRegister ? 'register' : 'login'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        })
        .then(res => res.json())
        .then(data => {
            setAuthenticationToken(data.token)
            router.refresh();
        })
        .catch(() => {
            throw new Error(`Error, unable to ${isRegister ? 'register' : 'login'}`);
        })

    }, [isRegister]);

    return (
      <div className="flex h-screen justify-center items-start pt-32">
        <Card className="w-auto">
            <CardHeader>
                <CardTitle>{isRegister ? 'Create an account' : 'Welcome back'}</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit}>
                    <Label>username</Label>
                    <Input type="text" name="username"/>
                    <Label>password</Label>
                    <Input type="password" name="password"/>
                    <div className="flex flex-col justify-end mt-5 gap-2">
                        <Button type="submit">
                            {isRegister ? 'Register' : 'Login'}
                        </Button>
                        <Button variant="secondary" onClick={(e) => { e.preventDefault(); setIsRegister(v => !v)}}>
                            {isRegister ? 'Login instead' : 'Register instead'}
                        </Button>
                    </div>
                </form>
            </CardContent>
        </Card>
      </div>
    );
}


