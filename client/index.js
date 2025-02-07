import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import app from './firebase-config.js'


const auth = getAuth(app);

const login = async (email, password) => {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Get the Firebase ID token
        const idToken = await user.getIdToken();
        console.log('Firebase ID Token:', idToken);

        // Send the token to your Flask backend
        const response = await fetch('http://localhost:5000/api/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: idToken }),
        });
        const data = await response.json();


        auth.currentUser = user
        console.log('Backend response:', data);

        console.log(auth.currentUser.uid);
        console.log(auth.currentUser.email);
    } catch (error) {
        console.error('Error signing in:', error.message);
    }
};

// Usage example
login('theolindh05@gmail.com', 'testing');