import cmd
from polar_is.plots import run_plot
from polar_is.data_object import DataObject

# Command-line interface for PolarIS
class PolarIsCLI(cmd.Cmd):
    prompt = "PolarIS $ "
    
    def __init__(self):
        super().__init__()
        # Dictionary to store data objects by name
        self.data_objects = {} 

    def do_quit(self, arg):
        print("Exiting.")
        return True

    def do_data_object(self, arg):
        # Expected format: data_object <name> <dataset> <variable> <start_t> <end_t> <t_res> <lat_range> <lon_range> <space_res> <aggregation>
        try:
            parts = arg.split()

            name = parts[0]
            dataset = parts[1]
            variable = parts[2]
            start_t = parts[3]
            end_t = parts[4]
            t_res = parts[5]

            lat_range = eval(parts[6])  
            lon_range = eval(parts[7])

            space_res = float(parts[8])
            aggregation = parts[9]

            obj = DataObject(
                name,
                dataset,
                variable,
                start_t,
                end_t,
                t_res,
                lat_range,
                lon_range,
                space_res,
                aggregation
            )

            self.data_objects[name] = obj
            print(f"Saved DataObject '{name}'")

        except Exception as e:
            print("Error creating DataObject:", e)

    def do_plot(self, arg):
        try:
            # Expected format: plot <data_object_name> <type> [filter value]
            parts = arg.split()

            if len(parts) < 2:
                print("Usage: plot <data_object_name> <type> [filter value]")
                return

            data_name = parts[0]
            plot_type = parts[1]


            if data_name not in self.data_objects:
                print(f"Error: DataObject '{data_name}' not found.")
                return

            data = self.data_objects[data_name]

            kwargs = {}


            if plot_type in ["find_time", "find_area"]:
                if len(parts) < 4:
                    print("Error: find_time and find_area require filter and value.")
                    return

                kwargs["filter"] = parts[2]
                kwargs["value"] = float(parts[3])

            print("Plotting...")


            result = run_plot(data, plot_type, **kwargs)

            print("Plot complete.")

            return result  

        except ValueError:
            print("Error: value must be a number.")
        except Exception as e:
            print("Plot error:", e)

def main():
    print("Starting PolarIS")
    PolarIsCLI().cmdloop()