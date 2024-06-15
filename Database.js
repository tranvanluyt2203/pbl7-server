// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAV9UDPynO_o-z6GH-zVZoKDaH3Tm-215E",
  authDomain: "pbl7-9ebca.firebaseapp.com",
  projectId: "pbl7-9ebca",
  storageBucket: "pbl7-9ebca.appspot.com",
  messagingSenderId: "599362391678",
  appId: "1:599362391678:web:7faf2d2e37d539c3bfd22f",
  measurementId: "G-DXT76N2QDM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);