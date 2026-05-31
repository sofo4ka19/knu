import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Auth0Provider } from '@auth0/auth0-react'
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <BrowserRouter>
            <Auth0Provider
                domain="dev-378024ihuz3ym3fa.auth0.com"
                clientId="vmR7WpZXtzyxIcaeldZvghYJjNyEK05V"
                authorizationParams={{
                    redirect_uri: window.location.origin,
                    audience: "https://car-rental-api"
                }}
            >
                <App />
            </Auth0Provider>
        </BrowserRouter>
    </StrictMode>
)