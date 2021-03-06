"""This module contains functions for managing and applying node colors in
Houdini.

"""

# =============================================================================
# IMPORTS
# =============================================================================

# Houdini Toolbox Imports
from ht.events import registerEventGroup
from ht.nodes.colors.event import ColorNodeEvent

# =============================================================================

# Register our event to handle automatic color setting.
registerEventGroup(ColorNodeEvent())

