import { useState, useRef } from "react";
import './Login.css'
import 'boxicons/css/boxicons.min.css'
import { useNavigate } from 'react-router-dom';
import { GoogleSignIn } from 'components/GoogleAuth'

export default function Login() {
    const [ passwordVisible, setPasswordVisible ] = useState(false);
    const navigate = useNavigate();
    const email = useRef<HTMLInputElement>(null);
    const password = useRef<HTMLInputElement>(null);


    const handleTogglePassword = () => {
        setPasswordVisible((prevStat) => !prevStat)
    }

    interface CustomElements extends HTMLFormControlsCollection   {
        email: HTMLInputElement;
        password: HTMLInputElement;
    }

    interface CustomForm extends HTMLFormElement {
        readonly elements: CustomElements;
    }
    
    const handleSubmit = async (e: React.FormEvent<CustomForm>)=> {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:5000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    "username": email.current?.value,
                    "password": password.current?.value
                })
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

    return (
        <section className="container-login">
            <div className="form">
                <div>
                    <header>Login</header>
                    <form onSubmit={handleSubmit}>
                        <div className="field input-field">
                            <input type="email" placeholder="Email" className="input" ref={email} />
                        </div>
                        <div className="field input-field">
                            <input type={passwordVisible ? 'text' : 'password'} placeholder="Password" className="password" ref={password} />
                            <i className={ `eye-icon bx ${passwordVisible ? 'bx-hide' : 'bx-show'}`} onClick={handleTogglePassword}></i>
                        </div>

                        <div className="form-link">
                            <a href="#" className="forgot-pass">Forgot password?</a>
                        </div>

                        <div className="field button-field">
                            <button>Login</button>
                        </div>
                    </form>

                    <div className="form-link">
                        <span>Don't have an account? <a href="#" className="link signup-link">Signup</a></span>
                    </div>
                </div>

                <div className="line"></div>
                <div className="media-options">
                    <GoogleSignIn />
                </div>

            </div>
        </section>
    )
}
