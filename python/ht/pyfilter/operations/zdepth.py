"""This module contains an operation to force a zdepth pass."""

# =============================================================================
# IMPORTS
# =============================================================================

# Houdini Toolbox Imports
from ht.pyfilter.logger import logger
from ht.pyfilter.operations.operation import PyFilterOperation, logFilter
from ht.pyfilter.property import getProperty, setProperty

#import mantra

# =============================================================================
# CLASSES
# =============================================================================

class ZDepthPass(PyFilterOperation):
    """Force the render to only contain C and Pz planes.

    As long as there is an extra image plane that is not C or Of this operation
    will remap an extra image plane to be Pz and disable the rest.

    This operation creates and uses the -zdepth arg.

    """

    def __init__(self, manager):
        super(ZDepthPass, self).__init__(manager)

        # Should the operation be run.
        self._active = False

        # We have not set the Pz plane yet.
        self.data["set_pz"] = False

    # =========================================================================
    # STATIC METHODS
    # =========================================================================

    @staticmethod
    def buildArgString(active):
        return "-zdepth"

    @staticmethod
    def registerParserArgs(parser):
        """Register interested parser args for this operation."""
        parser.add_argument(
            "-zdepth",
            action="store_true"
        )

    # =========================================================================
    # METHODS
    # =========================================================================

    @logFilter
    def filterCamera(self):
        """Apply camera properties."""
        # Redirect output image?
        pass

    @logFilter("object:name")
    def filterInstance(self):
        """Apply constant black shaders to objects."""
        matte = getProperty("object:matte")
        phantom = getProperty("object:phantom")
        surface = getProperty("object:surface")

        setProperty("object:overridedetail", True)

        if matte == "true" or surface == "matte" or phantom == "true":
            setProperty("object:phantom", 1)

        else:
            shader = "opdef:/Shop/v_constant clr 0 0 0".split()

            setProperty("object:surface", shader)
            setProperty("object:displace", None)

    @logFilter("plane:variable")
    def filterPlane(self):
        """Modify image planes to ensure one will output Pz.

        This will disable all planes that are not C and Pz.

        """
        channel = getProperty("plane:channel")

        # The if the plane is Pz then store that it is set.
        if channel == "Pz":
            self.data["set_pz"] = True

        # If we haven't found a Pz plane yet and this channel isn't a primary
        # output channel then we will force it to be Pz.
        if not self.data["set_pz"] and channel not in ("C", "Of"):
            setProperty("plane:variable", "Pz")
            setProperty("plane:vextype", "float")
            setProperty("plane:channel", "Pz")
            setProperty("plane:pfilter", "minmax min")
            setProperty("plane:quantize", None)
            self.data["set_pz"] = True

        # Disable any other planes.
        elif channel not in ("C", "Pz"):
            setProperty("plane:disable", True)

    def processParsedArgs(self, filter_args):
        """Process any of our interested arguments if they were passed."""
        if filter_args.zdepth is not None:
            self._active = filter_args.zdepth

    def shouldRun(self):
        """Only run if the flag was passed."""
        return self._active
