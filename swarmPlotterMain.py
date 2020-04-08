import swarmPlotter as shake
import argparse
import os
import logging as log



# -------------------- PARSER INITIALIZATION -------------------- #
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--heli", help="Output Helicorder (24h)", action="store_true")
parser.add_argument("-P", "--plot", help="Output Plot (10min)", action="store_true")
parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

# -------------------- VERBOSE ARGUMENTS -------------------- #
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")

if args.heli: #Do Heli
    print("Initializing Helicorder Mode")
    shake.makeHeli()

elif args.plot: #Do Plot
    print("Initializing Plot Mode")
    shake.makePlot()



# log.info("This should be verbose.")
# log.warning("This is a warning.")
# log.error("This is an error.")

