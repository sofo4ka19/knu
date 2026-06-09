import { useAuth0 } from '@auth0/auth0-react'
import { Link } from 'react-router-dom'

export default function Navbar() {
    const { isAuthenticated, user, loginWithRedirect, logout } = useAuth0()

    const roles = (user?.['https://car-rental-api/roles'] as string[]) ?? []
    const isAdmin = roles.includes('admin')

    return (
        <nav style={styles.nav}>
            <div style={styles.left}>
                <Link to={isAdmin ? '/admin' : '/'} style={styles.logo}>
                    🚗 CarRental
                </Link>
            </div>

            <div style={styles.right}>
                {isAuthenticated && !isAdmin && (
                    <Link to="/my-orders" style={styles.link}>
                        Мої замовлення
                    </Link>
                )}

                {isAuthenticated && isAdmin && (
                    <Link to="/admin" style={styles.link}>
                        Адмін панель
                    </Link>
                )}

                {!isAuthenticated ? (
                    <button
                        style={styles.button}
                        onClick={() => loginWithRedirect()}
                    >
                        Увійти
                    </button>
                ) : (
                    <div style={styles.userBlock}>
            <span style={styles.email}>
              {user?.name ?? user?.email}
            </span>
                        <button
                            style={{...styles.button, ...styles.logoutButton}}
                            onClick={() => logout({
                                logoutParams: { returnTo: window.location.origin }
                            })}
                        >
                            Вийти
                        </button>
                    </div>
                )}
            </div>
        </nav>
    )
}

const styles: Record<string, React.CSSProperties> = {
    nav: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '12px 24px',
        backgroundColor: '#1a1a2e',
        color: 'white',
        boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
    },
    left: {
        display: 'flex',
        alignItems: 'center',
        gap: '24px',
    },
    right: {
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
    },
    logo: {
        color: 'white',
        textDecoration: 'none',
        fontSize: '20px',
        fontWeight: 'bold',
    },
    link: {
        color: '#a0aec0',
        textDecoration: 'none',
        fontSize: '15px',
        transition: 'color 0.2s',
    },
    button: {
        padding: '8px 16px',
        backgroundColor: '#4a90e2',
        color: 'white',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        fontSize: '14px',
    },
    logoutButton: {
        backgroundColor: '#e53e3e',
    },
    userBlock: {
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
    },
    email: {
        color: '#a0aec0',
        fontSize: '14px',
    },
}