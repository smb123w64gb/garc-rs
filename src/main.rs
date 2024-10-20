use clap::Parser;
use clap::CommandFactory;

mod garc;

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[command(arg_required_else_help(true))]
#[command(version, about, long_about = None)]
struct Args {
    /// Name of the person to greet
    #[arg(short, long)]
    name: String,

    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u8,
}

fn main() {
    let args = Args::parse();
}
