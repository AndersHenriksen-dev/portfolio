#!/bin/bash
# Script to render all Quarto projects

echo "Rendering blogs..."
cd blogs
quarto render
cd ..

echo "Rendering projects..."
cd projects
quarto render

echo "All Quarto projects have been rendered!"
