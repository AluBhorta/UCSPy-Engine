from data.input_as_csv.parse_csv import generate_state_from_csv


def init():
    state = generate_state_from_csv()
    # print(state)
    print(f"Total number of sections = {len(state.sections)}")


if __name__ == "__main__":
    init()
    # run_ucsp(epochs=50, population_size=128, algo="ga")
