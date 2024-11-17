project(
  'cc2540',
)

cc = find_program('sdcc')
cctool = find_program('cc-tool', '../cc-tool/cc-tool')
ccflash = [cctool, '-v', '-e', '-w']

c_args = [
  '-I/usr/share/sdcc/include',
  '--std-sdcc99',
  '-mmcs51',
  '--model-medium',
  '--xram-loc 0x0000',
  '--xram-size 0x2000',
  '--iram-size 0x0100',
  '-DUART0',
  '-Wa,-glos',
  '-Wa,-p'
]

compiler = generator(
  cc,
  arguments: [
    c_args,
    '-o',
    '@OUTPUT@',
    '-c',
    '@INPUT@',
  ],
  output: '@BASENAME@.rel',
)

common = compiler.process(
  [
    'time.c',
    'uart.c',
    'usb.c',
    'usb_cdc_acm.c',
    'util.c',
  ],
)

test_blink = custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_blink.c'),
    common,
  ],
  output: 'test_blink.hex',
)

test_time = custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_time.c'),
    common,
  ],
  output: 'test_time.hex',
)

test_uart = custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_uart.c'),
    common,
  ],
  output: 'test_uart.hex',
)

test_usb = custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_usb.c'),
    common,
  ],
  output: 'test_usb.hex',
)

run_target(
  'blink',
  command: [ccflash, test_blink],
)

run_target(
  'time',
  command: [ccflash, test_time],
)

run_target(
  'uart',
  command: [ccflash, test_uart]
)

run_target(
  'usb',
  command: [ccflash, test_usb],
)