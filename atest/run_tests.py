import os
import sys
import robot

if __name__ == '__main__':
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_ROOT = os.path.join(THIS_DIR, 'results')
    if len(sys.argv) == 1:
        print("No test folder provided. Running all tests from ", THIS_DIR)
        sys.argv.append(THIS_DIR)
        
    # Adding the robotframeworkNL folder to the python path forces the development
    # version to be used instead of the one installed on your system. You will also
    # need to add this path to your IDE options when running from there.
    robot.run_cli(['--outputdir', OUTPUT_ROOT,
                   '--pythonpath', os.path.join(THIS_DIR, '..')]
                   + sys.argv[1:])
