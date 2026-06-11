import { useAuth0 } from '@auth0/auth0-react'
import { Link } from 'react-router-dom'

export default function Navbar() {
    const { isAuthenticated, user, loginWithRedirect, logout } = useAuth0()

    const roles = (user?.['https://car-rental-api/roles'] as string[]) ?? []
    const isAdmin = roles.includes('admin')

    return (
        <nav className="navbar">
            <Link to={isAdmin ? '/admin' : '/'} className="navbar-logo">
                🚗 CarRental
            </Link>

            <div className="navbar-right">
                {isAuthenticated && !isAdmin && (
                    <Link to="/my-orders" className="navbar-link">
                        Мої замовлення
                    </Link>
                )}
                {isAuthenticated && isAdmin && (
                    <Link to="/admin" className="navbar-link">
                        Адмін панель
                    </Link>
                )}

                {!isAuthenticated ? (
                    <button className="btn-nav btn-nav-login" onClick={() => loginWithRedirect()}>
                        Увійти
                    </button>
                ) : (
                    <div className="navbar-user">
                        <span className="navbar-username">{user?.name ?? user?.email}</span>
                        <button
                            className="btn-nav btn-nav-logout"
                            onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
                        >
                            Вийти
                        </button>
                    </div>
                )}
            </div>
        </nav>
    )
}
