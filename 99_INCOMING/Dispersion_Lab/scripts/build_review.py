"""Build bilingual review Markdown and an English DOCX with native equations.

CODE MAP — refresh with python scripts/update_code_index.py
  L0013  Module configuration / entry point
END CODE MAP
"""
from pathlib import Path
import re,subprocess,sys
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review';MD=ROOT/'assets/md'
sections=[
 ('theory_01','1. Physical processes','1. Physikalische Prozesse','space_time'),
 ('theory_02','2. The pinboard','2. Das Galtonbrett','binomial'),
 ('theory_03','3. Arrival times and injection','3. Ankunftszeiten und Zugabe','arrival'),
 ('theory_04','4. Grey-grain network','4. Netzwerk mit grauen Körnern','grain'),
 ('theory_05','5. Continuum interpretation','5. Kontinuumsinterpretation',None),
 ('theory_06','6. Mass markers and model limits','6. Massenteilchen und Modellgrenzen',None),
 ('grain_motion','7. Upward and slow pathways','7. Aufwärtswege und langsame Verbindungen',None),
 ('settings_map','8. Where the controls belong','8. Zuordnung der Einstellungen',None),
 ('references','9. References','9. Quellen',None),
]
captions={
 'space_time':'Three calculated trajectories and their arrival times for six rows, mean step time 1 s, time CV 0.6, seed 42. Directions and times are independent. Line heights in the arrival panel identify events; they are not mass rates.',
 'binomial':'Exact binomial outlet probabilities for 4 and 12 rows, with a = 1 mm. The number of markers changes sampling precision, not these population probabilities.',
 'arrival':'Calculated arrival histograms for 10,000 markers per case; n = 12, mean step time 1 s, CV = 0 or 0.6, injection duration 0 or 6 s, seed 42. Labels give exact population arrival-time variances. Bin width is 0.5 s. Vertical scales differ; compare widths rather than peak heights.',
 'grain':'Left: a four-row grey-grain network with default geometry. Right: schematic surface gap mapped to an equivalent tube diameter; the centreline and circular grains do not resolve a real three-dimensional pore cross-section.'}
for lang in ['en','de']:
 suffix='' if lang=='en' else '_de'
 title='Dispersion laboratory' if lang=='en' else 'Dispersionslabor'
 text=f'---\ntitle: "{title}"\nsubtitle: "'+('Theory and interface review · Version 2.4 · 30 October 2026' if lang=='en' else 'Theorie- und Oberflächenprüfung · Version 2.4 · 30. Oktober 2026')+'"\n---\n\n'
 for name,en,de,fig in sections:
  text+='\n# '+(de if lang=='de' else en)+'\n\n'
  body=(MD/(name+suffix+'.md')).read_text().replace('### ','## ')
  body=body.replace('N⁻¹ᐟ²','$N^{-1/2}$')
  text+=body+'\n'
  if fig:
   cap=captions[fig] if lang=='en' else 'Eigene schematische Darstellung bzw. Modellberechnung; Annahmen siehe Begleittext.'
   text+=f'\n![{cap}](../assets/figures/{fig}{suffix}.png){{width=6.2in}}\n'
 (OUT/('Theory_Review'+suffix+'.md')).write_text(text)
if '--markdown-only' in sys.argv:
 print('Bilingual review Markdown written to',OUT)
 sys.exit(0)
subprocess.run(['pandoc','Theory_Review.md','-o','Theory_Review.docx','--from','markdown+tex_math_dollars','--standalone'],cwd=OUT,check=True)
doc=Document(OUT/'Theory_Review.docx')
styles={s.name:s for s in doc.styles}
sec=doc.sections[0];sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=Inches(.8);sec.bottom_margin=Inches(.8);sec.left_margin=Inches(.9);sec.right_margin=Inches(.9)
for name in ['Normal','Body Text','First Paragraph','Compact']:
 style=styles[name]
 style.font.name='Calibri';style.font.size=Pt(11);style.font.color.rgb=RGBColor(0,0,0)
 style.paragraph_format.space_after=Pt(6);style.paragraph_format.line_spacing=1.05
for name,size in [('Title',26),('Subtitle',12),('Heading 1',17),('Heading 2',13),('Heading 3',12)]:
 style=styles[name];style.font.name='Calibri';style.font.size=Pt(size);style.font.color.rgb=RGBColor(0,0,0)
 style.paragraph_format.space_before=Pt(12);style.paragraph_format.space_after=Pt(7)
 style.paragraph_format.keep_with_next=True
# Begin the control map and bibliography on fresh pages; let scientific text flow.
for index,p in enumerate(doc.paragraphs):
 # Keep the sentence introducing a display equation with that equation.
 if index+1<len(doc.paragraphs) and doc.paragraphs[index+1]._p.xpath('./m:oMathPara'):
  p.paragraph_format.keep_with_next=True
 if p.style.name=='Heading 1' and p.text.startswith(('8.','9.')):
  p.paragraph_format.page_break_before=True
 if p.style.name=='Image Caption':
  p.paragraph_format.space_after=Pt(8);p.paragraph_format.keep_with_next=False
  for r in p.runs:r.font.size=Pt(9)
 # Keep equation blocks intact.
 if p._p.xpath('.//m:oMath'):
  p.paragraph_format.keep_together=True
  p.paragraph_format.space_after=Pt(7)
for table in doc.tables:
 table.autofit=False
 borders=OxmlElement('w:tblBorders')
 for side in ['top','left','bottom','right','insideH','insideV']:
  border=OxmlElement('w:'+side);border.set(qn('w:val'),'single');border.set(qn('w:sz'),'4');border.set(qn('w:color'),'BBBBBB');borders.append(border)
 table._tbl.tblPr.append(borders)
 widths=[1.6,2.15,2.95]
 for row in table.rows:
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for i,cell in enumerate(row.cells):
   cell.width=Inches(widths[i])
   for p in cell.paragraphs:
    p.paragraph_format.space_after=Pt(4)
    for r in p.runs:r.font.size=Pt(9.5)
 header=table.rows[0]._tr.get_or_add_trPr();header.append(OxmlElement('w:tblHeader'))
 for cell in table.rows[0].cells:
  for r in cell.paragraphs[0].runs:r.bold=True
# Compact the bibliography while preserving readable reference type.
reference_section=False
for p in doc.paragraphs:
 if p.style.name=='Heading 1' and p.text.startswith('9.'):
  reference_section=True
 elif reference_section and p.style.name not in ('Heading 1','Heading 2'):
  p.paragraph_format.space_after=Pt(4);p.paragraph_format.line_spacing=1.0
  for r in p.runs:r.font.size=Pt(10.5)
footer=sec.footer.paragraphs[0]
footer.alignment=2
r=footer.add_run('Dispersion laboratory · 2.4  |  ');r.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
# Original image alt text remains in DrawingML from Pandoc.
doc.core_properties.title='Dispersion laboratory: theory and interface review'
doc.core_properties.subject='Version 2.4: educational solute transport module'
doc.core_properties.author=''
doc.save(OUT/'Theory_Review.docx')
print(OUT/'Theory_Review.docx')
