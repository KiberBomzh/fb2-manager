use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
mod formatter {
    use pyo3::prelude::*;
    
    use std::path::PathBuf;
    use std::io::Write;
    use std::fs::File;
    use xmlformat::Formatter;
    
    #[pyfunction]
    fn prettify(path: &str) -> PyResult<()> {
    	let formatter = Formatter {
        	compress: false,
        	indent: 4,
        	keep_comments: true,
        	eof_newline: true,
    	};
    
    	let file_path: PathBuf = PathBuf::from(path);
    	let formatted_text = formatter.format_file(file_path.clone()).unwrap();
    	let mut file = File::create(file_path)?;
    	file.write_all(formatted_text.as_bytes())?;
    
    	Ok(())
    }

}