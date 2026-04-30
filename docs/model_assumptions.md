# Model Assumptions

1. 2D rectangular grid and explicit finite-difference diffusion.
2. Left boundary fixed concentration, other boundaries zero-flux.
3. Three homogeneous regions: concrete, interface, rock.
4. Degradation is phenomenological: `Deg = 1 - exp(-k * C * t)`.
5. Damage equals degradation and reduces modulus/strength linearly.
