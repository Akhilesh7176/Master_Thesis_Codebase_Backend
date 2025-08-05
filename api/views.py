from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import subprocess
import os


class RunSimulationView(APIView):
    """
    API endpoint to run the simulation script.
    """

    def post(self, request, *args, **kwargs):
        # Retrieve parameters from the request data
        params = {
            "--fol": request.data.get("--fol"),
            "--v0": request.data.get("--v0"),
            "--T": request.data.get("--T"),
            "--s0": request.data.get("--s0"),
            "--b": request.data.get("--b"),
            "--a": request.data.get("--a"),
        }

        # Check if 'fol' (vehicle ID) is provided
        veh_id = params.get("--fol")
        if not veh_id:
            return Response({"error": "'fol' parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Build the command string dynamically based on the provided parameters
        exec_command = [f"{key} {value}" for key, value in params.items() if value]
        exec_command = " ".join(exec_command)

        try:
            # Get the absolute path to the script
            script_path = os.path.join(os.path.dirname(__file__), "sim_visual.py")

            # Check if the script exists
            if not os.path.isfile(script_path):
                return Response(
                    {"error": f"Simulation script not found at {script_path}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Prepare the command to execute the script
            command = ["python3", script_path] + exec_command.split()
            print(command)

            # Run the command
            result = subprocess.run(command, capture_output=True, text=True, cwd=os.path.dirname(__file__))

            # Check if the script execution was successful
            if result.returncode != 0:
                return Response(
                    {"error": "Simulation script execution failed.", "details": result.stderr},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Return success response with script output
            return Response(
                {"message": result.stdout.strip()},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
