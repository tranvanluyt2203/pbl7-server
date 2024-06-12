// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDvhGEIwzhRd5Ke8nBlOeoGboyWnKwQPQQ",
  authDomain: "pbl7-2da30.firebaseapp.com",
  projectId: "pbl7-2da30",
  storageBucket: "pbl7-2da30.appspot.com",
  messagingSenderId: "87939519651",
  appId: "1:87939519651:web:a8e22c6934d4a00bfb5b16",
  measurementId: "G-2XW2M8D6KM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);