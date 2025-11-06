# EVA Demo

## Content

#### Data

| **File Name**           | **Description**                                  |
| ----------------------- | ------------------------------------------------ |
| `BBT.geojson`           | Outline of a fictive broad belt transect         |
| `grid.geojson`          | 7×10 grid within the BBT                         |
| `test_data_habitat.csv` | Test data for habitat (with density information) |
| `test_data_sp.csv`      | Test data for species (absence/presence only)    |

#### Scripts

| **File Name**             | **Description**           |
| ------------------------- | ------------------------- |
| `EVA_code_AQ_habitat.Rmd` | EVA code for habitat data |

## Issues & changes

#### Features: rarity & significance

| Feature		   		| name in script 			| original method 	  | method in demo  |
|--------------------------		|----------------			|-----------------	  |-----------------|
|LRF: Locally Rare Feature 		|Rare species    			| 5%>	     	  	  | hard coded list |
|ROF: Regularly Occurring Feature 	|Common species  			| 5%<	     	  	  | hard coded list |
|ESF:  Ecological Significant Feature	|ESS: ecological significant species    | hard coded list	  | hard coded list |
|HFS: habitat forming species 		|HFKS: habitat forming key species	| hard coded list 	  | hard coded list |
|SS: symbiotic species	 		|HFKS: habitat forming key species	| hard coded list 	  | hard coded list |
|HFS: habitat forming species 		|HFKS: habitat forming key species	| hard coded list 	  | hard coded list |
|RRF: regional rare features 		|Rarespec_reg   			| based on spatial rarity | hard coded list |
|NRF: national rare features 		|RareSpecList_nation   			| based on spatial rarity | hard coded list |

#### EVA: AQ Changes
- AQ7: Records with density 0 where considered as an observation in the old code, contributing to the count of features in the subzone (score 5 instead of 0). In the new code, species observation with density 0 will be singed 0 score.

#### EVA: total score changes

...

