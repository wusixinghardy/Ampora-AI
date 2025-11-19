import os
from typing import List, Union
import matplotlib
from src.LLM.ChatGPT import ChatGPTClient
from src.services.lecture import generate_lecture, generate_learning_objectives, get_visual_descriptions, get_scripts, get_bulletpoints

matplotlib.use("Agg")

def _build_visualization_prompt(description: str, output_path: str) -> tuple[str, str]:
    """
    Build system and user prompts used to ask the LLM for matplotlib code
    that generates a visualization and saves it to output_path.
    """
    system_prompt = (
        "You are a senior Python engineer and data visualization expert. "
        "Your job is to write self-contained Python scripts that generate static PNG "
        "images using matplotlib."
    )

    user_prompt = (
        "You will be given a natural language description of a slide visualization.\n"
        "Write a complete, runnable Python script that uses matplotlib to generate that visualization.\n\n"
        f"Visualization description:\n{description}\n\n"
        "Strict requirements:\n"
        "- Use only the Python standard library and matplotlib.\n"
        "- At the top of the script, set a non-interactive backend by doing:\n"
        "    import matplotlib\n"
        "    matplotlib.use('Agg')\n"
        "- Import matplotlib.pyplot as plt.\n"
        "- Create exactly one figure that matches the description as closely as possible.\n"
        f"- The script MUST call plt.savefig(r'{output_path}') at the end.\n"
        "- Do not call plt.show().\n"
        "- Do not print anything.\n"
        "- The script must be self-contained: if executed with 'python script.py', it should generate the image file.\n"
        "- Your entire reply must be ONLY Python code, with no backticks and no explanation."
    )

    return system_prompt, user_prompt


def _execute_generated_code(python_code: str) -> None:
    """
    Execute dynamically-generated Python code in an isolated namespace.

    WARNING: This runs arbitrary code. Only use this with trusted prompts and inputs.
    """
    exec_globals = {"__name__": "__main__"}
    exec(python_code, exec_globals)


def generate_visualizations_from_descriptions(
    visual_descriptions: List[str],
    output_dir: Union[str, os.PathLike] = "generated_visuals",
    model: str | None = None,
) -> List[str]:

    output_dir_str = os.fspath(output_dir)
    os.makedirs(output_dir_str, exist_ok=True)

    client = ChatGPTClient(model=model)
    output_paths: List[str] = []

    for idx, raw_description in enumerate(visual_descriptions, start=1):
        description = (raw_description or "").strip()
        if not description:
            raise ValueError(f"Visualization description for slide {idx} is empty.")

        filename = f"slide_{idx:02d}.png"
        full_path = os.path.abspath(os.path.join(output_dir_str, filename))

        system_prompt, user_prompt = _build_visualization_prompt(description, full_path)

        # 1) Ask the LLM to generate matplotlib code.
        try:
            python_code = client.chat(system_prompt, user_prompt)
        except Exception as e:
            raise RuntimeError(f"Failed to generate code for slide {idx}: {e}") from e

        # 2) Execute the generated code so it creates the image file.
        try:
            _execute_generated_code(python_code)
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute generated code for slide {idx}. "
                f"Generated code was:\n{python_code}\nError: {e}"
            ) from e

        # 3) Verify that the image file was actually created.
        if not os.path.exists(full_path):
            raise RuntimeError(
                f"Generated code for slide {idx} executed without raising an error, "
                f"but the expected image file was not found at: {full_path}"
            )

        output_paths.append(full_path)

    return output_paths


if __name__ == "__main__":
    # in the real pipeline we should do the following:
    #   from lecture import generate_learning_objectives, generate_lecture, get_visual_descriptions
    #   lecture_data = generate_lecture(...)
    #   visual_descriptions = get_visual_descriptions(lecture_data)
    #   generate_visualizations_from_descriptions(visual_descriptions)
    # topic = "Stochastic Gradient Descent"
    # objectives = generate_learning_objectives(topic)
    # lecture = generate_lecture(objectives)

    # scripts = get_scripts(lecture)
    # visuals = get_visual_descriptions(lecture)
    # bullets = get_bulletpoints(lecture)

    hardcoded_visuals = [
        "Title: Empirical Risk Minimization. Left side: a simple diagram of a dataset as a grid of small dots labeled x one through x n, each with an associated y label. Middle: a box labeled Model with parameter theta takes each x i and outputs predictions. Right side: a panel labeled Per-example loss ell of x i and y i with a simple bar chart showing losses for individual samples. Next to it, a larger panel titled Empirical risk equals average loss shows a big average bar being computed from the individual bars. Below all of this, a horizontal arrow flows from Dataset to Model to Loss to Average Loss, highlighting the pipeline. In the bottom right, a vector arrow labeled Gradient of full loss points downhill on a contour-like loss landscape with theta on the axes, illustrating the direction of steepest decrease.",
        "Three-part theoretical summary infographic. Left panel: Convex case. A smooth convex bowl with a path of iterates descending to the bottom. A label notes: diminishing learning rate; expected suboptimality decreases like one over square root of iterations. Middle panel: Nonconvex case. A rugged landscape with a path that settles in a flat basin. Annotation: expected gradient norm decreases like one over square root of iterations with diminishing learning rate. Right panel: Divergence scenarios. Illustration of overshooting steps bouncing around a steep valley with a red warning sign labeled too large learning rate. Additional icons show a burst symbol for high gradient variance and a scale icon for poor feature scaling. At the bottom, a checklist strip: LR schedule, variance control, regularization, clipping, monitoring."
    ]

    paths = generate_visualizations_from_descriptions(hardcoded_visuals)
    print("Generated images:", paths)