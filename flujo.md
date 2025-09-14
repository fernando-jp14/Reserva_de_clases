# Flujo de registro y sincronización con Google Calendar

## 1. Registrar usuario

**Endpoint:**  
`POST http://127.0.0.1:8000/api/usuarios/register/`

**Body ejemplo:**
```json
{
	"username": "usuario",
	"password": "contraseña"
}
```

---

## 2. Asignar membresía en el admin

- Ingresa al admin de Django.
- Edita el usuario recién creado y asigna la membresía:  
	- **FREE:** Solo puede reservar una clase por día.  
	- **PREMIUM:** Puede reservar ilimitadas clases y sincronizar con Google Calendar.

---

## 3. Obtener token JWT

**Endpoint:**  
`POST http://127.0.0.1:8000/api/token/`

**Body ejemplo:**
```json
{
	"username": "usuario",
	"password": "contraseña"
}
```

**Respuesta:**  
Recibirás los campos `access` y `refresh`.  
Usa el `access` token en la cabecera para autenticar tus siguientes peticiones:

```
Authorization: Bearer TU_ACCESS_TOKEN
```

---

## 4. Autorizar acceso a Google Calendar

**Endpoint:**  
`GET http://localhost:8000/api/usuarios/google-calendar/auth/`

- Haz una petición GET.
- El sistema te devolverá una URL de Google.
- Ingresa a esa URL, selecciona tu correo y autoriza la app.

---

## 5. Guardar el token de Google Calendar

**Endpoint:**  
`POST http://localhost:8000/api/usuarios/google-calendar/token/`

**Body ejemplo:**
```json
{
	"access_token": "token",
	"refresh_token": "token refresh",
	"token_expiry": "2025-09-12T19:49:11Z"
}
```

**Respuesta esperada:**
```json
{
	"detail": "Token guardado correctamente."
}
```

---

## 6. Reservar una clase

**Endpoint:**  
`POST http://127.0.0.1:8000/api/reservas/bookings/`

**Body ejemplo:**
```json
{
	"class_session_id": 1
}
```

- El usuario **PREMIUM**: la reserva se sincroniza automáticamente con Google Calendar.
- El usuario **FREE**: solo puede reservar una clase por día y no se sincroniza con Google Calendar.

---

**Notas:**
- El flujo de Google Calendar solo aplica para usuarios PREMIUM.
- Si necesitas el `refresh_token`, asegúrate de revocar el acceso en tu cuenta de Google antes de autorizar nuevamente.
- Todos los endpoints requieren autenticación JWT excepto el registro.
