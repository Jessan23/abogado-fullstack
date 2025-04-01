import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";

const Home = () => {
    const { store, actions } = useContext(Context);
    const [formData, setFormData] = useState({
        email: "",
        password: ""
    });

    const handleInputChange = (event) => {
        setFormData({ ...formData, [event.target.name]: event.target.value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        // Llamar a la acción de login
        const response = await actions.loginUser(formData);
        // Si el login es exitoso, redirigir o hacer algo con el token
        if (response.status === 200) {
            localStorage.setItem("token", store.token); // Guardar el token
            // Redirigir o actualizar el estado si es necesario
            // Aquí podrías redirigir a otro componente o actualizar la UI
            alert("Login exitoso");
        } else {
            alert("Error en el login");
        }
    };

    return (
        <div className="container mt-5">
            <h1>Bienvenido</h1>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input
                        type="email"
                        name="email"
                        className="form-control"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Contraseña</label>
                    <input
                        type="password"
                        name="password"
                        className="form-control"
                        value={formData.password}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Entrar</button>
            </form>
        </div>
    );
};

export default Home;
