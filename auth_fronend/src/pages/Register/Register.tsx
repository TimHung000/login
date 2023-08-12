import './Register.css'
import 'boxicons/css/boxicons.min.css'
import { useState, useRef } from "react"
import { useNavigate } from 'react-router-dom';
import { GoogleRegister } from 'components/GoogleAuth'


export default function Register() {
    const [ passwordVisible, setPasswordVisible ] = useState(false);
    const [ confirmPasswordVisible, setConfirmPasswordVisible ] = useState(false);
    const navigate = useNavigate()
    const handleTogglePassword = () => {
        setPasswordVisible((prevStat) => !prevStat)
    }
    const handleToggleConfirmPassword = () => {
        setConfirmPasswordVisible((prevStat) => !prevStat)
    }

    const email = useRef<HTMLInputElement>(null);
    const password = useRef<HTMLInputElement>(null);
    const confirmPassword = useRef<HTMLInputElement>(null);
    const name = useRef<HTMLInputElement>(null);
    
    interface CustomElements extends HTMLFormControlsCollection   {
        name: HTMLInputElement;
        email: HTMLInputElement;
        password: HTMLInputElement;
        confirmPassword: HTMLInputElement;
    }
    interface CustomForm extends HTMLFormElement {
        readonly elements: CustomElements;
    }

    const handleSubmit = async (e: React.FormEvent<CustomForm>) => {
        e.preventDefault();

        try {
            console.log(email.current?.value,)
            const response = await fetch('http://localhost:5000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name.current?.value,
                    email: email.current?.value,
                    password: password.current?.value,
                    confirmed_password: confirmPassword.current?.value
                })
            })

            if (!response.ok)
                throw new Error(`HTTP error! Status: ${response.status}`);
            
            navigate("/login");
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    return (
        <section className="container-register">
            {/* <!-- Signup Form --> */}
            <div className="form">
               <div>
                   <header>Signup</header>
                   <form onSubmit={handleSubmit}>
                        <div className="field input-field">
                           <input type="text" placeholder="name" className="input" ref={name}/>
                        </div>
                        <div className="field input-field">
                           <input type="email" placeholder="Email" className="input" ref={email}/>
                        </div>

                        <div className="field input-field">
                            <input type={passwordVisible ? 'text' : 'password'} placeholder="Password" className="password" ref={password}/>
                            <i className={ `eye-icon bx ${passwordVisible ? 'bx-hide' : 'bx-show'}`} onClick={handleTogglePassword}></i>
                        </div>

                        <div className="field input-field">
                            <input type={confirmPasswordVisible ? 'text' : 'password'} placeholder="Confirm password" className="password" ref={confirmPassword}/>
                            <i className={ `eye-icon bx ${confirmPasswordVisible ? 'bx-hide' : 'bx-show'}`} onClick={handleToggleConfirmPassword}></i>
                        </div>

                        <div className="field button-field">
                            <button>Signup</button>
                        </div>
                   </form>

                   <div className="form-link">
                       <span>Already have an account? <a href="#" className="link login-link">Login</a></span>
                   </div>
               </div>

               <div className="line"></div>

               <div className="media-options">
                    <GoogleRegister />
               </div>

           </div>
       </section>

    )
}
