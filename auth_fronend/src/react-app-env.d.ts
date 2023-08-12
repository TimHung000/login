// <reference types="react-scripts" />

declare global {
    interface Window {
        FB: any;
    }
}


declare namespace NodeJS {
    interface ReactEnv extends ProcessEnv {
        // NODE_ENV: 'development' | 'production' | 'test';
        // PUBLIC_URL: string;
        REACT_APP_GOOGLE_CLIENT_ID: string;
        REACT_APP_GOOGLE_CLIENT_SECRET: string;
        REACT_APP_GOOGLE_REDIRECT: string;
    }
  
    interface Process {
      env: ReactEnv;
    }
}