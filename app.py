
import streamlit as st
import re

from clases.datos import mascotas
from clases.usuario import Usuario
from clases.compatibilidad import Compatibilidad
from base_datos import (
    guardar_solicitud as guardar_en_base,
    obtener_solicitudes,
    actualizar_estado,
    crear_tabla_mensajes,
    guardar_mensaje,
    obtener_mensajes,
    marcar_mensaje_enviado
)
from correo import enviar_correo


# --------------------------------------------------
# CONFIGURACION
# --------------------------------------------------

st.set_page_config(
    page_title="PetMatch | Adopcion responsable",
    page_icon="🐾",
    layout="wide"
)

# Cambia esta clave por una propia antes de compartir
# o publicar el proyecto.
CLAVE_ADMIN = "PetMatchAdmin2026!"

crear_tabla_mensajes()

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False


# --------------------------------------------------
# ESTILO VISUAL
# --------------------------------------------------

st.markdown("""
<style>
    :root {
        --pm-green: #496b55;
        --pm-green-dark: #2f4f3b;
        --pm-green-soft: #eaf1e8;
        --pm-cream: #faf8f2;
        --pm-sand: #eee8dc;
        --pm-text: #26352b;
        --pm-muted: #718074;
    }

    .stApp {
        background: var(--pm-cream);
        color: var(--pm-text);
    }

    [data-testid="stHeader"] {
        background: rgba(250, 248, 242, 0.88);
    }

    .block-container {
        padding-top: 1.7rem;
        padding-bottom: 3.5rem;
        max-width: 1240px;
    }

    /* Encabezado principal */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 3.1rem 3rem;
        border: 1px solid #dce7d9;
        border-radius: 28px;
        background: linear-gradient(125deg, #e8f0e5 0%, #f5f1e8 58%, #f0e9dc 100%);
        margin: .6rem 0 1.2rem;
    }

    .hero .eyebrow {
        display: inline-block;
        padding: .38rem .78rem;
        border-radius: 999px;
        background: rgba(73, 107, 85, .11);
        color: var(--pm-green-dark);
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: .8rem;
    }

    .hero h1 {
        color: var(--pm-green-dark);
        font-size: clamp(2.3rem, 5vw, 3.5rem);
        font-weight: 800;
        letter-spacing: -.045em;
        line-height: 1.08;
        margin: 0 0 .75rem;
    }

    .hero p {
        color: #4c6251;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 720px;
        margin-bottom: .35rem;
    }

    /* Navegación */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: .35rem;
        padding: .45rem;
        border: 1px solid #e4e8df;
        border-radius: 16px;
        background: #fffdf9;
    }

    [data-testid="stTabs"] button[data-baseweb="tab"] {
        border-radius: 11px;
        padding: .65rem 1rem;
        color: #647365;
        font-weight: 600;
        transition: background .2s ease;
    }

    [data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        background: #f0f4ed;
        color: var(--pm-green-dark);
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        background: var(--pm-green-soft);
        color: var(--pm-green-dark);
    }

    [data-testid="stTabs"] button[aria-selected="true"] p {
        color: var(--pm-green-dark);
        font-weight: 700;
    }

    /* Tarjetas, métricas y formularios */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-color: #e4e8df !important;
        border-radius: 19px !important;
        background: rgba(255, 253, 249, .88);
    }

    div[data-testid="stMetric"] {
        background: #edf3e9;
        border: 1px solid #dfe8da;
        padding: 1.05rem 1.2rem;
        border-radius: 17px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: #657766;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--pm-green-dark);
        font-weight: 750;
    }

    [data-testid="stForm"] {
        padding: 1.2rem;
        border: 1px solid #e4e8df;
        border-radius: 19px;
        background: #fffdf9;
    }

    /* Botones */
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        border-radius: 12px;
        border: 1px solid #496b55;
        background: #496b55;
        color: white;
        font-weight: 650;
        min-height: 2.7rem;
        transition: all .18s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background: #2f4f3b;
        border-color: #2f4f3b;
        color: white;
        transform: translateY(-1px);
    }

    /* Campos */
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-baseweb="select"] > div {
        border-radius: 11px;
        border-color: #dfe5da;
        background: #fff;
    }

    h1, h2, h3 {
        color: var(--pm-green-dark);
        letter-spacing: -.025em;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--pm-muted);
    }

    hr {
        border-color: #e5e8df;
    }

    /* Fotos alineadas en tarjetas de mascotas y favoritas */
    [class*="st-key-mascota_"] [data-testid="stImage"] img,
    [class*="st-key-favorita_"] [data-testid="stImage"] img {
        display: block;
        width: 100%;
        height: 220px;
        object-fit: cover;
        object-position: center;
        border-radius: 15px;
    }

    /* Adaptación para pantallas pequeñas */
    @media (max-width: 700px) {
        .block-container { padding: 1rem 1rem 2rem; }
        .hero { padding: 2rem 1.35rem; border-radius: 21px; }
        .hero p { font-size: .98rem; }
        [data-testid="stTabs"] [data-baseweb="tab-list"] { gap: .15rem; }
        [data-testid="stTabs"] button[data-baseweb="tab"] { padding: .5rem .55rem; }
        [class*="st-key-mascota_"] [data-testid="stImage"] img,
        [class*="st-key-favorita_"] [data-testid="stImage"] img {
            height: 200px;
        }
    }

/* ==========================================
   PETMATCH - MEJORAR LEGIBILIDAD GENERAL
========================================== */

/* TEXTO GENERAL */
.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp li,
.stApp small {
    color: #263b2d !important;
}

.stButton > button,
[data-testid="stFormSubmitButton"] > button,
.stButton > button *,
[data-testid="stFormSubmitButton"] > button * {
    color: #ffffff !important;
}

/* PESTAÑAS DE NAVEGACIÓN */
[data-testid="stTabs"] button[role="tab"],
[data-testid="stTabs"] button[data-baseweb="tab"] {
    background-color: #f8f7f1 !important;
    color: #263b2d !important;
    border: 1px solid #cbd8c8 !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

[data-testid="stTabs"] button[role="tab"] *,
[data-testid="stTabs"] button[data-baseweb="tab"] * {
    color: #263b2d !important;
    font-weight: 800 !important;
}

/* PESTAÑA SELECCIONADA */
[data-testid="stTabs"] button[aria-selected="true"] {
    background-color: #355b43 !important;
    border-color: #355b43 !important;
}

[data-testid="stTabs"] button[aria-selected="true"] *,
[data-testid="stTabs"] button[aria-selected="true"] p {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* TÍTULOS Y ETIQUETAS DE LOS FORMULARIOS */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *,
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label,
.stRadio label,
.stCheckbox label {
    color: #263b2d !important;
    font-weight: 600 !important;
}

/* INDICACIONES Y AYUDAS */
[data-testid="stTooltipContent"],
[data-testid="stHelp"],
[data-testid="stCaptionContainer"] {
    color: #526657 !important;
}

/* CAMPOS PARA ESCRIBIR */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #263b2d !important;
    border: 1px solid #aebfae !important;
}

/* TEXTO DE EJEMPLO DENTRO DE LOS CAMPOS */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #68776a !important;
    opacity: 1 !important;
}

/* LISTAS DESPLEGABLES */
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #263b2d !important;
    border-color: #aebfae !important;
}

[data-baseweb="select"] * {
    color: #263b2d !important;
}

/* OPCIONES DE LAS LISTAS */
[role="listbox"],
[role="option"] {
    background-color: #ffffff !important;
    color: #263b2d !important;
}

/* TEXTO DE LOS RADIO BUTTONS Y CHECKBOXES */
[data-testid="stRadio"] label *,
[data-testid="stCheckbox"] label * {
    color: #263b2d !important;
}

/* MENSAJES DE AYUDA */
.stAlert p,
.stAlert span {
    color: #263b2d !important;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <span class="eyebrow">Adopción responsable · Salta</span>
    <h1>🐾 PetMatch</h1>
    <p><b>Una nueva amistad puede cambiar dos vidas.</b></p>
    <p>
        Encontrá a tu compañero ideal. Conocé mascotas, descubrí qué
        tan compatibles son con tu estilo de vida y empezá una historia
        de cariño y cuidado responsable.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("Un hogar, una oportunidad y mucho amor por compartir.")


# --------------------------------------------------
# PESTANAS PRINCIPALES
# --------------------------------------------------

(
    tab_inicio,
    tab_mascotas,
    tab_test,
    tab_solicitar,
    tab_estado,
    tab_admin
) = st.tabs([
    "🏠 Inicio",
    "🐶 Mascotas en adopcion",
    "💚 Test de compatibilidad",
    "📩 Solicitar adopcion",
    "🔎 Estado de solicitud",
    "🔐 Administracion"
])


# --------------------------------------------------
# INICIO
# --------------------------------------------------

with tab_inicio:
    st.header("Un encuentro que puede cambiarlo todo")

    st.write("""
    PetMatch es una plataforma pensada para facilitar la adopcion
    responsable de mascotas. Nuestro objetivo es ayudar a las
    personas a encontrar un compañero que se adapte a su estilo de vida.
    """)

    st.subheader("¿Cómo funciona PetMatch?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1.🐚 Conoce")
        st.write(
            "Conoce las mascotas en adopcion y sus "
            "cualidades, personalidades y necesidades."
        )

    with col2:
        st.markdown("### 2.🫧 Descubre")
        st.write(
            "Responde el test para conocer que mascotas "
            "podrian adaptarse a tu vida."
        )

    with col3:
        st.markdown("### 3.🐇 Adopta")
        st.write(
            "Completa la solicitud y consulta su estado "
            "mientras se revisa tu pedido."
        )

    st.divider()

    st.subheader("Nuestro compromiso")

    st.write("""
    Creemos que adoptar es una decision importante. Por eso,
    buscamos promover el cuidado, el respeto y la responsabilidad
    hacia los animales, teniendo en cuenta que cada mascota
    necesita tiempo, atencion y un hogar adecuado.
    """)

    st.info(
        "Explora las pestañas para conocer a las mascotas, "
        "hacer el test o enviar una solicitud de adopcion."
    )


# --------------------------------------------------
# MASCOTAS EN ADOPCION Y FAVORITOS
# --------------------------------------------------

with tab_mascotas:
    st.header("🐾 Conoce nuestras mascotas")
    st.write(
        "Utiliza los filtros para encontrar mascotas "
        "que coincidan con tus preferencias."
    )

    opciones_especie = sorted({mascota.especie for mascota in mascotas})
    opciones_tamano = sorted({mascota.tamaño for mascota in mascotas})
    opciones_personalidad = sorted(
        {mascota.personalidad for mascota in mascotas}
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        filtro_especie = st.selectbox(
            "Especie",
            ["Todas"] + opciones_especie,
            key="filtro_especie_v2"
        )

    with col2:
        filtro_tamano = st.selectbox(
            "Tamano",
            ["Todos"] + opciones_tamano,
            key="filtro_tamano_v2"
        )

    with col3:
        filtro_personalidad = st.selectbox(
            "Personalidad",
            ["Todas"] + opciones_personalidad,
            key="filtro_personalidad_v2"
        )

    mascotas_filtradas = [
        mascota for mascota in mascotas
        if (filtro_especie == "Todas" or mascota.especie == filtro_especie)
        and (filtro_tamano == "Todos" or mascota.tamaño == filtro_tamano)
        and (
            filtro_personalidad == "Todas"
            or mascota.personalidad == filtro_personalidad
        )
    ]

    st.caption(
        f"Encontramos {len(mascotas_filtradas)} mascota(s)."
    )

    if mascotas_filtradas:
        columnas = st.columns(3)

        for i, mascota in enumerate(mascotas_filtradas):
            with columnas[i % 3]:
                with st.container(
                    border=True,
                    key=f"mascota_{mascota.nombre}"
                ):
                    st.subheader(f"🐾 {mascota.nombre}")
                    st.image(
                        mascota.imagen,
                        width="stretch"
                    )

                    st.write(f"**Especie:** {mascota.especie}")
                    st.write(f"**Edad:** {mascota.edad} años")
                    st.write(f"**Tamaño:** {mascota.tamaño}")
                    st.write(
                        f"**Personalidad:** {mascota.personalidad}"
                    )
                    st.write(
                        f"**Actividad:** {mascota.nivel_actividad}"
                    )

                    es_favorita = (
                        mascota.nombre in st.session_state.favoritos
                    )

                    texto_boton = (
                        "❤️ Quitar de favoritos"
                        if es_favorita
                        else "🤍 Agregar a favoritos"
                    )

                    if st.button(
                        texto_boton,
                        key=f"favorito_{mascota.nombre}",
                        width="stretch"
                    ):
                        if es_favorita:
                            st.session_state.favoritos.remove(
                                mascota.nombre
                            )
                        else:
                            st.session_state.favoritos.append(
                                mascota.nombre
                            )

                        st.rerun()
    else:
        st.warning(
            "No encontramos mascotas con esos filtros. "
            "Proba con otras opciones."
        )

    st.divider()
    st.subheader("❤️ Mis favoritas")

    mascotas_favoritas = [
        mascota for mascota in mascotas
        if mascota.nombre in st.session_state.favoritos
    ]

    if mascotas_favoritas:
        columnas = st.columns(3)

        for i, mascota in enumerate(mascotas_favoritas):
            with columnas[i % 3]:
                with st.container(
                    border=True,
                    key=f"favorita_{mascota.nombre}"
                ):
                    st.image(
                        mascota.imagen,
                        width="stretch"
                    )
                    st.write(f"**{mascota.nombre}**")
                    st.write(mascota.personalidad)

                    if st.button(
                        "Quitar de favoritos",
                        key=f"quitar_{mascota.nombre}"
                    ):
                        st.session_state.favoritos.remove(
                            mascota.nombre
                        )
                        st.rerun()
    else:
        st.info(
            "Todavia no guardaste favoritas. "
            "Puedes hacerlo desde las tarjetas de mascotas."
        )


# --------------------------------------------------
# TEST DE COMPATIBILIDAD
# --------------------------------------------------

with tab_test:
    st.header("💚 Test de compatibilidad")

    st.write("""
    Responde algunas preguntas para conocer que mascotas
    podrian ser compatibles con tu hogar y tus preferencias.
    """)

    with st.form("formulario_compatibilidad"):
        nombre_test = st.text_input("¿Como te llamas?")

        edad = st.number_input(
            "¿Cuantos años tenes?",
            min_value=1,
            max_value=120,
            value=18
        )

        vivienda = st.selectbox(
            "¿Vives en casa o departamento?",
            ["Casa", "Departamento"]
        )

        tiempo = st.selectbox(
            "¿Cuanto tiempo tienes disponible?",
            ["Poco", "Medio", "Mucho"]
        )

        actividad = st.selectbox(
            "¿Que personalidad prefieres?",
            ["Tranquilo", "Activo", "Indiferente"]
        )

        otros_animales = st.radio(
            "¿Tienes otros animales en casa?",
            ["Sí", "No"]
        )

        enviar_test = st.form_submit_button(
            "Encontrar mi mascota ideal 🐾",
            width="stretch"
        )

    if enviar_test:
        if not nombre_test.strip():
            st.warning("Escribe tu nombre para continuar.")
        else:
            usuario = Usuario(
                nombre_test.strip(),
                edad,
                vivienda,
                tiempo,
                otros_animales
            )

            resultados = []

            for mascota in mascotas:
                calculo = Compatibilidad(usuario, mascota)
                porcentaje = calculo.calcular(actividad)
                resultados.append((mascota, porcentaje))

            resultados.sort(
                key=lambda resultado: resultado[1],
                reverse=True
            )

            st.subheader(
                f"Resultados para {nombre_test.strip()}"
            )

            st.write(
                "Estas son las mascotas ordenadas de mayor "
                "a menor compatibilidad."
            )

            for mascota, porcentaje in resultados:
                with st.container(border=True):
                    col_foto, col_info = st.columns([1, 2])

                    with col_foto:
                        st.image(
                            mascota.imagen,
                            width="stretch"
                        )

                    with col_info:
                        st.subheader(
                            f"{mascota.nombre}: {porcentaje}%"
                        )
                        st.progress(
                            max(0, min(float(porcentaje), 100)) / 100
                        )
                        st.write(
                            f"**Especie:** {mascota.especie}"
                        )
                        st.write(
                            f"**Personalidad:** {mascota.personalidad}"
                        )

                        if porcentaje == resultados[0][1]:
                            st.success(
                                "Una de tus mayores compatibilidades."
                            )

            st.info(
                "El resultado es orientativo. Antes de adoptar, "
                "considera las necesidades reales de la mascota."
            )


# --------------------------------------------------
# SOLICITAR ADOPCION
# --------------------------------------------------

with tab_solicitar:
    st.header("🏡 Solicitar una adopcion")

    st.write("""
    Completa el formulario para que podamos registrar tu interes
    en adoptar una mascota. Enviaremos tu solicitud al sistema
    para que pueda ser revisada.
    """)

    with st.form("formulario_adopcion"):
        nombre_adoptante = st.text_input("Nombre completo")
        email_adoptante = st.text_input("Correo electronico")

        mascota_elegida = st.selectbox(
            "¿Que mascota te gustaria adoptar?",
            [mascota.nombre for mascota in mascotas]
        )

        motivo = st.text_area(
            "¿Por que te gustaria adoptar esta mascota?"
        )

        enviar_solicitud = st.form_submit_button(
            "Enviar solicitud 💚",
            width="stretch"
        )

    if enviar_solicitud:
        email_limpio = email_adoptante.strip()

        email_valido = re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email_limpio
        )

        if (
            not nombre_adoptante.strip()
            or not email_limpio
            or not motivo.strip()
        ):
            st.warning(
                "Completa tu nombre, correo y motivo de adopcion."
            )
        elif not email_valido:
            st.warning("Escribe una direccion de correo valida.")
        else:
            id_nueva_solicitud = guardar_en_base(
                nombre_adoptante.strip(),
                mascota_elegida,
                motivo.strip(),
                email_limpio
            )

            st.success(
                f"Tu solicitud para {mascota_elegida} "
                "se registró correctamente."
            )

            st.info(
                f"Tu número de solicitud es **{id_nueva_solicitud}**. "
                "Guardalo junto con el correo que utilizaste para "
                "consultar el estado más adelante."
            )


# --------------------------------------------------
# CONSULTA PUBLICA DEL ESTADO
# --------------------------------------------------

with tab_estado:
    st.header("🔎 Consulta el estado de tu solicitud")

    st.write("""
    Para consultar tu solicitud, ingresa el numero que te indique
    el equipo de PetMatch y el correo que utilizaste al registrarte.
    """)

    with st.form("formulario_consulta_estado"):
        id_consulta = st.number_input(
            "Numero de solicitud",
            min_value=1,
            step=1
        )

        email_consulta = st.text_input(
            "Correo electronico utilizado en la solicitud"
        )

        consultar = st.form_submit_button(
            "Consultar estado",
            width="stretch"
        )

    if consultar:
        email_busqueda = email_consulta.strip().lower()

        solicitud_encontrada = None

        for solicitud in obtener_solicitudes():
            if (
                solicitud[0] == int(id_consulta)
                and (solicitud[5] or "").strip().lower()
                == email_busqueda
            ):
                solicitud_encontrada = solicitud
                break

        if solicitud_encontrada:
            st.success("Encontramos tu solicitud.")

            st.write(
                f"**Numero:** {solicitud_encontrada[0]}"
            )
            st.write(
                f"**Mascota:** {solicitud_encontrada[2]}"
            )
            st.write(
                f"**Estado:** {solicitud_encontrada[4]}"
            )

            estado = solicitud_encontrada[4]

            if estado == "Pendiente":
                st.info(
                    "Tu solicitud esta pendiente de revision."
                )
            elif estado == "Aprobada":
                st.success(
                    "Tu solicitud fue aprobada. "
                    "El equipo debera contactarte para coordinar "
                    "los siguientes pasos."
                )
            elif estado == "Rechazada":
                st.warning(
                    "La solicitud no fue aprobada. "
                    "Puedes comunicarte con el equipo para recibir "
                    "mas informacion."
                )
        else:
            st.error(
                "No encontramos una solicitud con esos datos. "
                "Revisa el numero y el correo."
            )


# --------------------------------------------------
# ADMINISTRACION PRIVADA
# --------------------------------------------------

with tab_admin:
    st.header("🔐 Administracion de PetMatch")

    st.write(
        "Esta seccion es para el equipo encargado de revisar "
        "solicitudes y contactar a los adoptantes."
    )

    if not st.session_state.admin_autenticado:
        with st.form("formulario_acceso_admin"):
            clave_ingresada = st.text_input(
                "Clave de administrador",
                type="password"
            )

            iniciar_sesion = st.form_submit_button(
                "Ingresar",
                width="stretch"
            )

        if iniciar_sesion:
            if clave_ingresada == CLAVE_ADMIN:
                st.session_state.admin_autenticado = True
                st.rerun()
            else:
                st.error("La clave ingresada no es correcta.")

    else:
        if st.button("Cerrar sesion de administrador"):
            st.session_state.admin_autenticado = False
            st.rerun()

        solicitudes_admin = obtener_solicitudes()

        st.divider()
        st.subheader("📋 Solicitudes recibidas")

        if solicitudes_admin:
            total = len(solicitudes_admin)
            pendientes = sum(
                1 for s in solicitudes_admin
                if s[4] == "Pendiente"
            )
            aprobadas = sum(
                1 for s in solicitudes_admin
                if s[4] == "Aprobada"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Total", total)
            col2.metric("Pendientes", pendientes)
            col3.metric("Aprobadas", aprobadas)

            for solicitud in solicitudes_admin:
                (
                    id_solicitud,
                    nombre,
                    mascota,
                    motivo,
                    estado,
                    email
                ) = solicitud

                with st.container(border=True):
                    st.subheader(
                        f"Solicitud N.º {id_solicitud}"
                    )

                    st.write(f"**Adoptante:** {nombre}")
                    st.write(f"**Correo:** {email or 'No registrado'}")
                    st.write(f"**Mascota:** {mascota}")
                    st.write(f"**Motivo:** {motivo}")
                    st.write(f"**Estado actual:** {estado}")

                    estados_validos = [
                        "Pendiente",
                        "Aprobada",
                        "Rechazada"
                    ]

                    with st.form(
                        f"form_estado_{id_solicitud}"
                    ):
                        nuevo_estado = st.selectbox(
                            "Cambiar estado",
                            estados_validos,
                            index=(
                                estados_validos.index(estado)
                                if estado in estados_validos
                                else 0
                            ),
                            key=f"estado_admin_{id_solicitud}"
                        )

                        guardar_estado = st.form_submit_button(
                            "Guardar estado"
                        )

                    if guardar_estado:
                        actualizado = actualizar_estado(
                            id_solicitud,
                            nuevo_estado
                        )

                        if actualizado:
                            st.success(
                                "Estado actualizado correctamente."
                            )
                            st.rerun()
                        else:
                            st.error(
                                "No se pudo actualizar el estado."
                            )

                    st.markdown("#### 💌 Mensajes para el adoptante")

                    with st.form(
                        f"form_mensaje_{id_solicitud}"
                    ):
                        texto_mensaje = st.text_area(
                            "Escribir mensaje",
                            key=f"texto_admin_{id_solicitud}",
                            placeholder=(
                                "Hola, queremos coordinar una reunion "
                                "para que conozcas a tu posible compañero."
                            )
                        )

                        guardar_texto = st.form_submit_button(
                            "Guardar y enviar mensaje"
                        )

                    if guardar_texto:
                        if not texto_mensaje.strip():
                            st.warning(
                                "Escribe un mensaje antes de guardarlo."
                            )
                        elif not email or not email.strip():
                            st.error(
                                "Esta solicitud no tiene un correo "
                                "de destino. No se puede enviar."
                            )
                        else:
                            guardado = guardar_mensaje(
                                id_solicitud,
                                texto_mensaje.strip()
                            )

                            if not guardado:
                                st.error(
                                    "No se pudo guardar el mensaje "
                                    "en la base de datos."
                                )
                            else:
                                mensajes_actuales = obtener_mensajes(
                                    id_solicitud
                                )
                                if mensajes_actuales:
                                    id_mensaje_nuevo = mensajes_actuales[0][0]
                                    asunto = (
                                        f"PetMatch - Solicitud N.º "
                                        f"{id_solicitud}"
                                    )
                                    enviado_ok, resultado_envio = enviar_correo(
                                        email,
                                        asunto,
                                        texto_mensaje.strip()
                                    )

                                    if enviado_ok:
                                        marcado = marcar_mensaje_enviado(
                                            id_mensaje_nuevo
                                        )
                                        if marcado:
                                            st.success(
                                                "Mensaje guardado y correo "
                                                "enviado correctamente."
                                            )
                                        else:
                                            st.warning(
                                                "Gmail aceptó el envío, pero "
                                                "no se pudo actualizar el "
                                                "registro del mensaje."
                                            )
                                    else:
                                        st.warning(
                                            "El mensaje quedó guardado en "
                                            "PetMatch, pero no se pudo enviar "
                                            "el correo. " + resultado_envio
                                        )
                                else:
                                    st.error(
                                        "El mensaje se guardó, pero no se "
                                        "pudo recuperar para enviarlo."
                                    )

                    if email:
                        st.caption("Correo de destino: " + email)
                    else:
                        st.warning(
                            "Esta solicitud no tiene correo registrado."
                        )

                    historial = obtener_mensajes(id_solicitud)

                    with st.expander("Ver historial de mensajes"):
                        if historial:
                            for registro in historial:
                                (
                                    id_mensaje,
                                    texto,
                                    fecha,
                                    enviado
                                ) = registro

                                st.caption(f"Fecha: {fecha}")
                                st.write(texto)

                                if enviado:
                                    st.success("Correo enviado")
                                else:
                                    st.caption(
                                        "Guardado en PetMatch; correo "
                                        "pendiente de envío."
                                    )
                                    if email:
                                        if st.button(
                                            "Reintentar envío",
                                            key=f"reenviar_{id_mensaje}"
                                        ):
                                            asunto = (
                                                f"PetMatch - Solicitud N.º "
                                                f"{id_solicitud}"
                                            )
                                            enviado_ok, resultado_envio = (
                                                enviar_correo(
                                                    email,
                                                    asunto,
                                                    texto
                                                )
                                            )
                                            if enviado_ok:
                                                if marcar_mensaje_enviado(
                                                    id_mensaje
                                                ):
                                                    st.success(
                                                        "Correo enviado "
                                                        "correctamente."
                                                    )
                                                    st.rerun()
                                                else:
                                                    st.warning(
                                                        "El correo se envió, "
                                                        "pero no se pudo "
                                                        "actualizar el registro."
                                                    )
                                            else:
                                                st.error(resultado_envio)

                                st.divider()
                        else:
                            st.info(
                                "Todavia no hay mensajes guardados."
                            )

        else:
            st.info("Todavia no hay solicitudes registradas.")

    st.divider()
    st.caption(
        "PetMatch · Panel de administracion"
    )


# --------------------------------------------------
# PIE DE PAGINA
# --------------------------------------------------

st.divider()

st.caption(
    "🐾 PetMatch | Promoviendo la adopcion responsable"
)
