project (
  'cc2540',
)

cc = find_program('sdcc')

c_args = [
  '-std=c99',
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
    'delay.c',
    'time.c',
    'uart.c',
    'usb.c',
    'usb_cdc_acm.c',
    'util.c',
  ],
)

custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_blink.c'),
    common,
  ],
  output: 'test_blink.hex',
)

custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_time.c'),
    common,
  ],
  output: 'test_time.hex',
)

custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_uart.c'),
    common,
  ],
  output: 'test_uart.hex',
)

custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [
    compiler.process('test_usb.c'),
    common,
  ],
  output: 'test_usb.hex',
)