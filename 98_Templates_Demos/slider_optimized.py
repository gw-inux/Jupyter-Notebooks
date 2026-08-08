import streamlit as st
import numpy as np


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def _update_value(value_key, widget_key):
    """Copy the current widget value to the permanent parameter state."""
    st.session_state[value_key] = float(st.session_state[widget_key])


def parameter_input(
    label,
    key,
    default,
    min_value,
    max_value,
    *,
    step=None,
    scale="linear",
    use_number_input=False,
    number_format=None,
    log_steps_per_decade=20,
):
    """
    Parameter input that can switch between slider and number input
    while preserving the current value.

    scale="linear":
        Standard linear slider.

    scale="log":
        Logarithmically spaced slider using physical parameter values.
        The corresponding number input uses an automatically scaled
        additive step.
    """

    # -------------------------------------------------------------------------
    # Basic checks
    # -------------------------------------------------------------------------

    if scale not in ("linear", "log"):
        raise ValueError("scale must be 'linear' or 'log'.")

    if min_value >= max_value:
        raise ValueError("min_value must be smaller than max_value.")

    if not min_value <= default <= max_value:
        raise ValueError("default must be between min_value and max_value.")

    if scale == "log" and min_value <= 0:
        raise ValueError("Logarithmic parameters must be positive.")

    # -------------------------------------------------------------------------
    # Permanent parameter state
    # -------------------------------------------------------------------------

    value_key = f"{key}__value"

    if value_key not in st.session_state:
        st.session_state[value_key] = float(default)

    current_value = float(st.session_state[value_key])

    # Defensive clipping
    current_value = min(
        max(current_value, float(min_value)),
        float(max_value)
    )

    st.session_state[value_key] = current_value

    # =========================================================================
    # NUMBER INPUT
    # =========================================================================

    if use_number_input:

        widget_key = f"_{key}__number"

        # Synchronize temporary widget with permanent value
        st.session_state[widget_key] = current_value

        # ---------------------------------------------------------------------
        # Determine number-input step
        # ---------------------------------------------------------------------

        if step is not None:

            # Explicitly supplied step
            number_step = float(step)

        elif scale == "log":

            # Automatically adapt step to order of magnitude.
            #
            # Examples:
            # 7.94e-6 -> 1e-7
            # 3.20e-5 -> 1e-6
            # 4.50e-4 -> 1e-5
            # 2.00e-3 -> 1e-4

            exponent = np.floor(np.log10(current_value))

            number_step = 10.0 ** (exponent - 1)

        else:

            number_step = 0.01

        kwargs = {
            "label": label,
            "min_value": float(min_value),
            "max_value": float(max_value),
            "step": float(number_step),
            "key": widget_key,
            "on_change": _update_value,
            "args": (value_key, widget_key),
        }

        if number_format is not None:
            kwargs["format"] = number_format

        elif scale == "log":
            kwargs["format"] = "%.2e"

        st.number_input(**kwargs)

    # =========================================================================
    # LINEAR SLIDER
    # =========================================================================

    elif scale == "linear":

        widget_key = f"_{key}__slider"

        st.session_state[widget_key] = current_value

        kwargs = {
            "label": label,
            "min_value": float(min_value),
            "max_value": float(max_value),
            "key": widget_key,
            "on_change": _update_value,
            "args": (value_key, widget_key),
        }

        if step is not None:
            kwargs["step"] = float(step)

        if number_format is not None:
            kwargs["format"] = number_format

        st.slider(**kwargs)

    # =========================================================================
    # LOGARITHMIC SLIDER
    # =========================================================================

    else:

        widget_key = f"_{key}__slider"

        # Number of logarithmic decades
        decades = (
            np.log10(max_value)
            - np.log10(min_value)
        )

        n_intervals = max(
            1,
            int(round(decades * log_steps_per_decade))
        )

        # Generate logarithmically spaced physical values
        options = np.logspace(
            np.log10(min_value),
            np.log10(max_value),
            n_intervals + 1,
        )

        # ---------------------------------------------------------------------
        # Preserve arbitrary number-input values
        #
        # If the user entered a value such as 7.94e-6, this value will
        # normally not occur on the predefined logarithmic grid.
        #
        # Add it temporarily so switching back to the slider does NOT
        # change the parameter.
        # ---------------------------------------------------------------------

        if not np.any(
            np.isclose(
                options,
                current_value,
                rtol=1e-12,
                atol=0.0,
            )
        ):
            options = np.append(
                options,
                current_value
            )

        options = np.unique(
            np.sort(options)
        ).tolist()

        st.session_state[widget_key] = current_value

        st.select_slider(
            label,
            options=options,
            key=widget_key,
            format_func=lambda x: f"{x:.2e}",
            on_change=_update_value,
            args=(value_key, widget_key),
        )

    # -------------------------------------------------------------------------
    # Return the physical parameter value
    # -------------------------------------------------------------------------

    return float(st.session_state[value_key])


# =============================================================================
# TEST APPLICATION
# =============================================================================

st.title("Slider / Number Input Test")

st.write(
    "Switch between slider and number input. "
    "The parameter values should remain unchanged."
)

number_input = st.toggle(
    "Use number input instead of sliders",
    value=False,
)


# -----------------------------------------------------------------------------
# LINEAR PARAMETER
# -----------------------------------------------------------------------------

st.subheader("Linear parameter")

linear_value = parameter_input(
    label="Linear parameter",
    key="linear_parameter",
    default=50.0,
    min_value=0.0,
    max_value=100.0,
    step=1.0,
    scale="linear",
    use_number_input=number_input,
    number_format="%.1f",
)

st.write(f"Value = {linear_value}")


# -----------------------------------------------------------------------------
# LOGARITHMIC PARAMETER
# -----------------------------------------------------------------------------

st.subheader("Logarithmic parameter")

log_value = parameter_input(
    label="Hydraulic conductivity $K$ [m/s]",
    key="log_parameter",
    default=1e-4,
    min_value=1e-7,
    max_value=1e-2,
    scale="log",
    use_number_input=number_input,
    log_steps_per_decade=20,
)

st.write(f"Value = {log_value:.3e}")