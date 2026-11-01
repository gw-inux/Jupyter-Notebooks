"""Browser regression for autoplay, completion, multilingual math and mobile.

CODE MAP — refresh with python scripts/update_code_index.py
  L0036  ready
  L0041  screenshot_stable
  L0050  run_and_focus
  L0070  click
  L0079  nav
  L0080  number
  L0082  expand
  L0086  steering
  L0088  complete
END CODE MAP
"""
from pathlib import Path
import json,re,subprocess,sys,time,urllib.request,tempfile
from playwright.sync_api import sync_playwright,expect,Error
expect.set_options(timeout=20000)
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(tempfile.mkdtemp(prefix='dispersion-v24-browser-'))
report={};servers=[]
try:
 for app,port in [('app.py',8511),('multipage_example.py',8512)]:
  log=(OUT/f'server_{port}.log').open('w')
  servers.append(subprocess.Popen([sys.executable,'-m','streamlit','run',app,'--server.port',str(port),'--server.address','127.0.0.1','--server.headless','true','--browser.gatherUsageStats','false'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT))
  for _ in range(100):
   try:urllib.request.urlopen(f'http://127.0.0.1:{port}/_stcore/health',timeout=.5);break
   except OSError:time.sleep(.1)
  else:raise RuntimeError('Startup failed')
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1280,'height':950})
  errors=[];bad=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:bad.append([r.status,r.url]) if r.status>=400 else None)
  def ready():
   page.wait_for_timeout(350)
   page.wait_for_function("document.querySelector('[data-testid=stApp]')?.getAttribute('data-test-script-state')==='notRunning'",timeout=45000)
   assert page.get_by_test_id('stException').count()==0
   assert page.locator('.katex-error').count()==0
  def screenshot_stable(locator,path):
   # A language/navigation refresh can replace an image while Playwright waits
   # for fonts. Retry only that detached-element capture, not failed assertions.
   for attempt in range(3):
    try:
     locator.screenshot(path=str(path));return
    except Error as exc:
     if 'not attached to the DOM' not in str(exc) or attempt==2:raise
     ready()
  def run_and_focus(key):
   stage=key.removeprefix('disp_').rsplit('_',1)[0]
   boards=page.locator('figure[id^="disp-transport-'+stage+'-"]')
   old=boards.first.get_attribute('id') if boards.count() else ''
   page.locator('.st-key-'+key+' button').click()
   page.wait_for_function("""([stage,old]) => {
     const boards=[...document.querySelectorAll('figure[id^="disp-transport-'+stage+'-"]')];
     const heading=document.getElementById('disp-observe-'+stage);
     return heading && boards.some(b=>b.id!==old && window.__dispersionFocusedRuns?.has(b.id))
       && heading.getBoundingClientRect().top>=45 && heading.getBoundingClientRect().top<180;
   }""",arg=[stage,old],timeout=35000)
   board=page.locator('figure[id^="disp-transport-'+stage+'-"]').last
   page.wait_for_timeout(950)
   top=page.locator('#disp-observe-'+stage).evaluate('(b)=>b.getBoundingClientRect().top')
   assert 45<=top<180,(key,top)
   button=page.locator('.st-key-disp_'+stage+'_run button').bounding_box()
   assert button['y']>=0 and button['y']+button['height']<page.viewport_size['height'],button
   assert page.get_by_test_id('stException').count()==0
   report.setdefault('new_run_focus',[]).append(key)
   print('Observe heading and Run visible:',key,flush=True)
  def click(key):
   if key.endswith(('_run','_new')):
    run_and_focus(key)
   else:
    # Streamlit tooltips include an invisible copy of their child button.
    page.locator('.st-key-'+key+' button:visible').click()
    if key.endswith('_pause'):
     expect(page.locator('.st-key-'+key.removesuffix('_pause')+'_play button')).to_be_enabled()
    ready()
  def nav(key):click('nav_'+key)
  def number(key,value):
   el=page.locator('.st-key-'+key+' input');el.fill(str(value));el.press('Enter');ready()
  def expand(label):
   el=page.get_by_test_id('stExpander').filter(has=page.locator('summary',has_text=label)).first
   if el.locator('details').get_attribute('open') is None:el.locator('summary').click()
   return el
  def steering():
   return expand('Progress through the experiment')
  def complete(key):
   steering();click(key+'_complete')
   expect(page.locator('[class*="st-key-'+key+'_seek_"] [role=slider]')).to_have_attribute('aria-valuenow','100',timeout=20000)
   expect(page.locator('img.dispersion-plot')).to_have_count(3)
   expect(page.locator('img[alt="Outlet distributions"],img[alt="Auslassverteilungen"]')).to_be_visible()
  page.goto('http://127.0.0.1:8511')
  expect(page.get_by_role('heading',name='Dispersion laboratory',exact=True)).to_be_visible(timeout=30000);ready()
  page.screenshot(path=str(OUT/'overview.png'),full_page=True)
  nav('principles')
  expand('The pinboard principle and its equations')
  assert page.locator('.katex-display').count()==5
  expect(page.get_by_text('The mean and variance follow',exact=False)).to_be_visible()
  page.screenshot(path=str(OUT/'principles_math.png'),full_page=True)
  expand('The physical Galton board')
  page.wait_for_function("[...document.querySelectorAll('img')].every(i=>i.complete&&i.naturalWidth>0)")
  expect(page.locator('img.dispersion-plot')).to_have_count(2)
  expect(page.locator('img[alt="Transport board ready"]')).to_be_visible()
  assert page.locator('.st-key-disp_guided_run').locator('xpath=ancestor::details').count()==0
  click('disp_guided_run');steering()
  expect(page.locator('.st-key-disp_guided_pause button')).to_be_enabled()
  expect(page.locator('.st-key-disp_guided_step button')).to_be_disabled()
  page.wait_for_timeout(1000);click('disp_guided_pause')
  expect(page.locator('.st-key-disp_guided_play button')).to_be_enabled()
  expect(page.locator('.st-key-disp_guided_step button')).to_be_enabled()
  caption=page.get_by_text(re.compile('^t = .*Not yet injected:')).inner_text()
  assert not caption.startswith('t = 0 s'),caption
  click('disp_guided_reset');click('disp_guided_step')
  expect(page.get_by_text(re.compile('^t = 1 s ·'))).to_be_visible()
  click('disp_guided_previous')
  expect(page.get_by_text(re.compile('^t = 0 s ·'))).to_be_visible()
  click('disp_guided_play');click('disp_guided_pause')
  complete('disp_guided')
  expect(page.get_by_text(re.compile('^t = 20 s .*Collected: 1'))).to_be_visible()
  page.locator('img.dispersion-plot').nth(1).screenshot(path=str(OUT/'guided_board.png'))
  expand('Progress through the experiment').screenshot(path=str(OUT/'controls.png'))
  start=page.locator('.st-key-disp_guided_reset button:visible')
  expect(start).to_contain_text('Start')
  assert start.bounding_box()['width']>=140
  assert start.locator('p').evaluate('(e)=>e.scrollWidth<=e.clientWidth'), 'Start label clipped'
  report['start_label_fits']=True
  assert page.locator('[class*=st-key-disp_guided_save], [class*=st-key-disp_guided_csv], [class*=st-key-disp_guided_json]').count()==0
  report['guided_empty_board_pause_step_and_no_exports']=True
  expect(page.locator('.st-key-disp_guided_run button')).to_contain_text('Rerun highlighted particles')
  click('disp_guided_run');complete('disp_guided')
  expect(page.get_by_text('Particle realization seed: 43',exact=True)).to_be_visible()
  report['guided_rerun_changes_seed']=True
  nav('pinboard')
  number('disp_pinboard_highlighted',10)
  page.get_by_role('combobox').first.click();page.get_by_role('option',name='Pinboard · variable travel times',exact=True).click();ready()
  click('disp_pinboard_run');complete('disp_pinboard')
  number('disp_pinboard_background_each',1000)
  expect(page.locator('img.dispersion-plot')).to_have_count(2)
  click('disp_pinboard_run');complete('disp_pinboard')
  page.screenshot(path=str(OUT/'pinboard_completed.png'),full_page=True)
  expect(page.get_by_text(re.compile('^t = .*Collected: 10,010'))).to_be_visible(timeout=15000)
  click('lang_de');nav('references');nav('pinboard')
  expect(page.get_by_text(re.compile('^t = .*Gesammelt: 10,010'))).to_be_visible()
  report['pinboard_population_and_navigation']=True
  nav('principles');expand('Das Galtonbrett-Prinzip und seine Gleichungen')
  assert page.locator('.katex-display').count()==5 and page.locator('.katex-error').count()==0
  click('lang_fr');expect(page.get_by_role('heading',name='Principles and guided experiment',exact=True)).to_be_visible()
  click('lang_en');nav('explore')
  preview=page.locator('figure.dispersion-preview')
  ratio=preview.evaluate('(e)=>e.getBoundingClientRect().width/e.parentElement.getBoundingClientRect().width')
  assert .79<ratio<.81,ratio
  screenshot_stable(preview,OUT/'grain_preview.png')
  titles=page.get_by_test_id('stExpander').locator('summary').all_text_contents()
  assert all(word in titles[i] for i,word in enumerate(['How to use','Board and transport','Particles and injection']))
  colour=page.locator('.st-key-disp_section_blue_explore_board summary').evaluate('(e)=>getComputedStyle(e).backgroundColor')
  assert colour=='rgb(237, 244, 248)',colour
  report['preview_scale_order_and_theme']=True
  click('disp_explore_run')
  started=time.monotonic()
  page.mouse.wheel(0,350);page.wait_for_timeout(300)
  board=page.locator('figure[id^="disp-transport-explore-"]').last
  top=board.evaluate('(e)=>e.getBoundingClientRect().top')
  page.wait_for_timeout(1100)
  assert abs(board.evaluate('(e)=>e.getBoundingClientRect().top')-top)<5
  report['animation_does_not_pull_scroll_back']=True
  # Observe the default 60-second grain display clock reaching its natural end.
  # Wait for the numerical completion condition, not a transient button label.
  print('Waiting for natural completion of the 60-second grain animation.',flush=True)
  expect(page.get_by_text(re.compile('^t = .*Collected: 1'))).to_be_visible(timeout=80000)
  expect(page.locator('.st-key-disp_explore_play button')).to_be_enabled(timeout=15000)
  report['grain_completion_wait_after_focus_s']=round(time.monotonic()-started,3)
  ready();expect(page.locator('img.dispersion-plot')).to_have_count(3)
  report['natural_completion_retains_board_and_distributions']=True
  expand('Optional display settings')
  expect(page.locator('.st-key-disp_explore_play_seconds [role=slider]')).to_have_attribute('aria-valuenow','60')
  report['grain_default_60_seconds']=True
  expand('Repeat, compare, and download')
  with page.expect_download() as info:page.get_by_role('button',name='Parameters and statistics · JSON',exact=True).click()
  target=OUT/'download.json';info.value.save_as(target)
  metadata=json.loads(target.read_text());assert metadata['config']['mode']=='grains'
  assert metadata['config']['rows']==20 and metadata['version']=='2.4.0'
  report['json_download']=True
  click('disp_explore_save');click('disp_explore_new')
  expect(page.locator('.st-key-disp_explore_pause button')).to_be_attached()
  complete('disp_explore')
  group=expand('Repeat, compare, and download')
  expect(group.get_by_text(re.compile('^Saved: grains; 20 rows; 1 markers; seed 42'))).to_be_visible()
  with page.expect_download() as info:page.get_by_role('button',name='Parameters and statistics · JSON',exact=True).click()
  target=OUT/'new_realization.json';info.value.save_as(target)
  assert json.loads(target.read_text())['config']['seed']==43
  report['save_and_new_realization_preserve_comparison']=True
  number('disp_explore_spacing_mm',1.5)
  expect(page.locator('img.dispersion-plot')).to_have_count(2)
  click('disp_explore_run');complete('disp_explore')
  page.get_by_test_id('stSidebar').hover()
  page.get_by_test_id('stSidebarCollapseButton').locator('button').click()
  page.set_viewport_size({'width':390,'height':844});ready()
  page.get_by_role('heading',name='Observe the transport',exact=True).scroll_into_view_if_needed()
  page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
  page.locator('img.dispersion-plot').nth(2).screenshot(path=str(OUT/'mobile_results.png'))
  assert page.evaluate('document.documentElement.scrollWidth')<=390
  report['mobile_no_horizontal_overflow']=True
  other=browser.new_page()
  other.goto('http://127.0.0.1:8512')
  expect(other.get_by_role('heading',name='Dispersion laboratory',exact=True)).to_be_visible(timeout=30000)
  other.get_by_role('link',name='Pinboard',exact=True).click()
  expect(other.locator('.st-key-disp_pinboard_run button')).to_be_visible(timeout=30000)
  other.locator('.st-key-disp_pinboard_run button').click()
  expect(other.locator('.st-key-disp_pinboard_pause button')).to_be_attached(timeout=30000)
  report['parent_integration']=True
  assert not errors and not bad,(errors,bad)
  report['javascript_errors']=errors;report['http_errors']=bad
  browser.close()
 (OUT/'browser_report.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({'output':str(OUT),'checks':report},indent=2))
except Exception:
 try:
  page.screenshot(path=str(OUT/'failure.png'),full_page=True)
  (OUT/'failure_text.txt').write_text(page.locator('body').inner_text())
 except Exception:pass
 raise
finally:
 (OUT/'browser_report_partial.json').write_text(json.dumps(report,indent=2))
 print('QA output:',OUT,flush=True)
 for server in servers:server.terminate();server.wait(timeout=10)
