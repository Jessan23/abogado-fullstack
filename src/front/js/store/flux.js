const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            user: null,
            clientes: [],
        },
        actions: {
            // Acción para obtener información del usuario
            getUser: async () => {
                try {
                    const resp = await fetch(process.env.BACKEND_URL + "/api/user");
                    const data = await resp.json();
                    setStore({ user: data }); // Actualiza el estado del usuario
                } catch (error) {
                    console.log("Error fetching user:", error);
                }
            },
            // Acción para obtener la lista de clientes
            getClientes: async () => {
                try {
                    const resp = await fetch(process.env.BACKEND_URL + "/clientes");
                    const data = await resp.json();
                    setStore({ clientes: data }); // Actualiza el estado de los clientes
                } catch (error) {
                    console.log("Error fetching clientes:", error);
                }
            },
            // Modificación de un cliente específico
            updateCliente: async (id, clienteData) => {
                try {
                    const resp = await fetch(process.env.BACKEND_URL + "/clientes/" + id, {
                        method: 'PUT',
                        body: JSON.stringify(clienteData),
                        headers: { 'Content-Type': 'application/json' }
                    });
                    const data = await resp.json();
                    // Si es exitoso, actualizamos el estado de los clientes
                    setStore({ clientes: data });
                } catch (error) {
                    console.log("Error updating cliente:", error);
                }
            },
            registerUser: async (formData) => {
				try {
					// Verificar que formData solo tenga los campos correctos
					const { email, password } = formData; // Solo desestructuramos correo y password
			
					console.log("Datos enviados para el registro:", { email, password }); // Verifica los datos
			
					const response = await fetch(process.env.BACKEND_URL + "/users", {
						method: "POST",
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify({ email, password }) // Solo enviamos correo y password
					});
			
					const data = await response.json();
			
					if (response.ok) {
						// Almacenar la información del usuario en el store
						setStore({
							user: data.user
						});
			
						return { status: 201 }; // Usuario registrado correctamente
					} else {
						// Si el servidor responde con un error, muestra el error en consola
						console.log("Error al registrar usuario:", data);
						return { status: response.status }; // Retorna el status del error
					}
				} catch (error) {
					console.error("Error al registrar usuario", error);
					return { status: 500 }; // Error del servidor
				}
			}
			
        }
    };
};

export default getState;
