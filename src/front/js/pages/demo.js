import React, { useState, useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";

export const Demo = () => {
    const { store, actions } = useContext(Context);

    // Estado local para el formulario
    const [formData, setFormData] = useState({
        nombre: '',
        email: '',
        password: ''
    });

    // Manejar cambios en los campos del formulario
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    // Manejar el envío del formulario de registro
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Llamar a la acción para registrar el usuario
        try {
            const response = await actions.registerUser(formData);
            if (response.status === 201) {
                alert("Usuario registrado exitosamente!");
            } else {
                alert("Hubo un problema al registrar el usuario.");
            }
        } catch (error) {
            console.error("Error durante el registro", error);
            alert("Ocurrió un error durante el registro.");
        }
    };

    return (
        <div className="container">
            <h1>Formulario de Registro</h1>
            <br />
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="nombre">Nombre</label>
                    <input
                        type="text"
                        className="form-control"
                        id="nombre"
                        name="nombre"
                        value={formData.nombre}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="correo">Correo</label>
                    <input
                        type="email"
                        className="form-control"
                        id="correo"
                        name="correo"
                        value={formData.correo}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Contraseña</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary mt-3">
                    Registrar
                </button>
            </form>
            <br />
            <Link to="/">
                <button className="btn btn-secondary">Volver al inicio</button>
            </Link>
        </div>
    );
};
