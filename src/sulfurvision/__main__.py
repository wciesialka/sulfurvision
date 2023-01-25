'''Main module responsible for handling terminal interaction.'''

# This file is part of sulfurvision.
# sulfurvision is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# version 3 of the License. sulfurvision is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details. You should have received a copy of the GNU General Public License along with
# sulfurvision. If not, see <https://www.gnu.org/licenses/>.

import argparse
from . import image_search
from . import image_maker

def main():
    '''Main method responsible for handling terminal interaction.
    '''
    parser = argparse.ArgumentParser(description="Generate a Sulfur Vision image.")
    parser.add_argument('-o', '--output', required=True,
                        type=argparse.FileType('wb'), help="Output file.")
    parser.add_argument('query', help='Search query.', type=str)
    args = parser.parse_args()

    search_result = image_search.search(args.query)

    if search_result is None:
        print("Could not find a result.")
    else:
        image = image_maker.make_image(search_result, args.query.upper())
        image.save(args.output)

if __name__ == "__main__":
    main()
