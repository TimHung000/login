import 'boxicons/css/boxicons.min.css'
import { useRef, useEffect } from "react";
import { useSearchParams, useNavigate } from 'react-router-dom';

const getGoogleAuthorizaion = async (redirect_uri: string) => {
    const oauth2Endpoint = `https://accounts.google.com/o/oauth2/v2/auth`;
    
    const params = {
        redirect_uri: redirect_uri,
        client_id: process.env.REACT_APP_GOOGLE_CLIENT_ID,
        response_type: "code",
        access_type: "offline",
        include_granted_scopes: "true",
        prompt: "consent",
        scope: [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
        ].join(" "),
    };

    const queryString = Object.entries(params).map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join('&')
    const googleUrl = `${oauth2Endpoint}?${queryString.toString()}`;
    window.location.replace(googleUrl) 
};

export const GoogleSignIn = () => {
    const currentGoogleAuthCode = useRef<string | null>(null)
    const navigate = useNavigate();
    const [queryParams] = useSearchParams()

    const handleGoogleSignIn = async () => {
        getGoogleAuthorizaion("http://localhost:3000/login");
    }

    const relayGoogleAuthToBackend = async () => {
        const authorizationCode = queryParams.get("code")
        if(authorizationCode != null && authorizationCode != "" && authorizationCode != currentGoogleAuthCode.current) {
            currentGoogleAuthCode.current = authorizationCode

            try {
                const response = await fetch("http://localhost:5000/auth/google-login", {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ "google_oauth2_code": authorizationCode }),
                })
    
                if (!response.ok)
                    throw new Error(`HTTP error! Status: ${response.status}`);
                

                const data = await response.json();
                if(data.access_token) {
                    localStorage.setItem('access_token', data.access_token);
                    navigate("/");
                } else
                    console.log('didn\'t get access token');
            
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }

    useEffect(() => {
        relayGoogleAuthToBackend()
    }, []);

    return (
        <button className="google-button media-option" onClick={handleGoogleSignIn}>
            sign in with Google
        </button>
    );
}


export const GoogleRegister = () => {
    const currentGoogleAuthCode = useRef<string | null>(null)
    const navigate = useNavigate();
    const [queryParams] = useSearchParams()

    const handleGoogleRegister = async () => {
        getGoogleAuthorizaion("http://localhost:3000/register");
    };

    const relayGoogleAuthToBackend = async () => {
        const authorizationCode = queryParams.get("code")
        if(authorizationCode != null && authorizationCode != "" && authorizationCode != currentGoogleAuthCode.current) {
            currentGoogleAuthCode.current = authorizationCode

            try {
                const response = await fetch("http://localhost:5000/auth/google-register", {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ "google_oauth2_code": authorizationCode }),
                })
    
                if (!response.ok)
                    throw new Error(`HTTP error! Status: ${response.status}`);

                navigate("\login");

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }

    useEffect(() => {
        relayGoogleAuthToBackend()
    }, []);

    return (
        <button className="google-button media-option" onClick={handleGoogleRegister}>
            register with Google
        </button>
    );
}

