// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCHShheA5Sjz31d7KhE-JdUB5xUnrfQlMQ",
    authDomain: "biljard-elo.firebaseapp.com",
    projectId: "biljard-elo",
    storageBucket: "biljard-elo.firebasestorage.app",
    messagingSenderId: "201889527124",
    appId: "1:201889527124:web:249d8ff8c45ee0128f44c1",
    measurementId: "G-J3V149T6S5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export default app