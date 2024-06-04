module tb_skeleton_final;

	// Local parameters to be
	// fed into the module
	// All except LBP_LENGTH and NB_CLASSES should be powers of 2!
	localparam int D = 1024;
	//localparam real p_sparse = 0.0078125;
	localparam int E = 64;
	localparam int LENGTH_SEGMENT = 128;
	localparam int NB_OF_SEGMENTS = 8;
	localparam int NB_TO_BUNDLE_IN_TIME = 256;
	localparam int LBP_LENGTH = 6;
	localparam int NB_CLASSES = 2;
	localparam int vector_fold_factor = 1;
	localparam int channel_fold_factor = 1;

	// Wirings	
	logic                          clk;
	logic                          arst_n_in;
	logic         [LBP_LENGTH-1:0] LBP_codes [E-1:0];


	logic 			       classification_ready;
	logic [$clog2(NB_CLASSES)-1:0] classification;
	logic                  [0:D-1] ictal_hv_in = 1024'b1110110110100000001100000111011010100010100011111111010001100110010001101100011000001011111010100010111101000101010111000010100000011100111001110011010011110010110111000101010101010111011110111100111010001110110101000100101111101111100011111010100100100101101101101100011100101111100100110100101101110111110101001101001110100010111110000100001110101010100110111000010010011010100010010100001001101111101010101101111100110101101011001101101101111000011101000111010011010001011001010011100001001011100010111000011100001011101110100011100100110110100000111011000000110011010100101111010011100001001000100100010011100111110010100010100001100110011000111100001110010101111010001000100101001101001000011111010000011111101101001000110111010010001110001110001010010101010010001111010001000100010001011000101011110111010100100001100100101010100110101101100010011111101000110000001010010111001001110110101010110010001011000111011100111010000000111110110101011001001000001010011111100101100100100100111110011011010010001100011001111001;
	logic                  [0:D-1] interictal_hv_in = 1024'b1111110110110000001100000101011000100010000011111111010000100010010001101110001000001011111000100010111001100101010111000010110000011100011101110001000011110010110101110101010101010111011110111100111000001110110001010000101011001110100011110010100101100001101101101100011100101110100100110100101100110011111101001101001110100000111110000110001110100010100110111000011010011010110000010100001001101111111010101101111100110101101011001001100001111000111100100111010010110001011001010011001000001010100010111000011100001011101110100011100100100110100010111011000000110011011100101111010011111001001000000100110011100111100010110010100001100110011001111100001010010101111010000100100101101101001000011111010010011110101100001000110111010010011110001110001010011101010010001111010101001100010011011000101011100111010100100001100100101010000110101101100010011011000001110010011010010111001001111110101010110010011011000111111101011010000000101111110111011001000000001010011111100101100100100110111110011011111010101100011101111101;



	logic use_mem;
	logic write_mem;
	logic [$clog2(D):0] ictal_sim;
	logic [$clog2(D):0] interictal_sim;





	integer               data_file    ; // file handler
	integer               scan_file    ; // file handler
	`define NULL 0

	// Clock level toggles every 10ns
	always begin #100ns; clk <= !clk; end //1953125ns for 512Hz


skeleton_final # (
		.D( D ),
		//.p_sparse( p_sparse ),
		.E( E ),
		.NB_SEGMENTS( NB_OF_SEGMENTS ),
		.LENGTH_SEGMENT( LENGTH_SEGMENT ),
		.NB_TO_BUNDLE_IN_TIME( NB_TO_BUNDLE_IN_TIME ),
		.LBP_LENGTH( LBP_LENGTH ),
		.NB_CLASSES( NB_CLASSES ),
		.vector_fold_factor( vector_fold_factor ),
		.channel_fold_factor( channel_fold_factor )
	) skeleton_unit (
		.clk 		      ( clk        ),
		.arst_n_in	      ( arst_n_in  ),
		.LBP_codes63            ( LBP_codes[63] ),
		.LBP_codes62            ( LBP_codes[62] ),
		.LBP_codes61            ( LBP_codes[61] ),
		.LBP_codes60            ( LBP_codes[60] ),
		.LBP_codes59            ( LBP_codes[59] ),
		.LBP_codes58            ( LBP_codes[58] ),
		.LBP_codes57            ( LBP_codes[57] ),
		.LBP_codes56            ( LBP_codes[56] ),
		.LBP_codes55            ( LBP_codes[55] ),
		.LBP_codes54            ( LBP_codes[54] ),
		.LBP_codes53            ( LBP_codes[53] ),
		.LBP_codes52            ( LBP_codes[52] ),
		.LBP_codes51            ( LBP_codes[51] ),
		.LBP_codes50            ( LBP_codes[50] ),
		.LBP_codes49            ( LBP_codes[49] ),
		.LBP_codes48            ( LBP_codes[48] ),
		.LBP_codes47            ( LBP_codes[47] ),
		.LBP_codes46            ( LBP_codes[46] ),
		.LBP_codes45            ( LBP_codes[45] ),
		.LBP_codes44            ( LBP_codes[44] ),
		.LBP_codes43            ( LBP_codes[43] ),
		.LBP_codes42            ( LBP_codes[42] ),
		.LBP_codes41            ( LBP_codes[41] ),
		.LBP_codes40            ( LBP_codes[40] ),
		.LBP_codes39            ( LBP_codes[39] ),
		.LBP_codes38            ( LBP_codes[38] ),
		.LBP_codes37            ( LBP_codes[37] ),
		.LBP_codes36            ( LBP_codes[36] ),
		.LBP_codes35            ( LBP_codes[35] ),
		.LBP_codes34            ( LBP_codes[34] ),
		.LBP_codes33            ( LBP_codes[33] ),
		.LBP_codes32            ( LBP_codes[32] ),
		.LBP_codes31            ( LBP_codes[31] ),
		.LBP_codes30            ( LBP_codes[30] ),
		.LBP_codes29            ( LBP_codes[29] ),
		.LBP_codes28            ( LBP_codes[28] ),
		.LBP_codes27            ( LBP_codes[27] ),
		.LBP_codes26            ( LBP_codes[26] ),
		.LBP_codes25            ( LBP_codes[25] ),
		.LBP_codes24            ( LBP_codes[24] ),
		.LBP_codes23            ( LBP_codes[23] ),
		.LBP_codes22            ( LBP_codes[22] ),
		.LBP_codes21            ( LBP_codes[21] ),
		.LBP_codes20            ( LBP_codes[20] ),
		.LBP_codes19            ( LBP_codes[19] ),
		.LBP_codes18            ( LBP_codes[18] ),
		.LBP_codes17            ( LBP_codes[17] ),
		.LBP_codes16            ( LBP_codes[16] ),
		.LBP_codes15            ( LBP_codes[15] ),
		.LBP_codes14            ( LBP_codes[14] ),
		.LBP_codes13            ( LBP_codes[13] ),
		.LBP_codes12            ( LBP_codes[12] ),
		.LBP_codes11            ( LBP_codes[11] ),
		.LBP_codes10            ( LBP_codes[10] ),
		.LBP_codes9             ( LBP_codes[9] ),
		.LBP_codes8             ( LBP_codes[8] ),
		.LBP_codes7             ( LBP_codes[7] ),
		.LBP_codes6             ( LBP_codes[6] ),
		.LBP_codes5             ( LBP_codes[5] ),
		.LBP_codes4             ( LBP_codes[4] ),
		.LBP_codes3             ( LBP_codes[3] ),
		.LBP_codes2             ( LBP_codes[2] ),
		.LBP_codes1             ( LBP_codes[1] ),
		.LBP_codes0             ( LBP_codes[0] ),
		.ictal_hv_in          ( ictal_hv_in ),
		.interictal_hv_in     ( interictal_hv_in ),
		.classification_ready ( classification_ready ),
		.classification       ( classification ),
                .send_next_LBP        ( send_next_LBP ),
		.ictal_sim	      ( ictal_sim ),
		.interictal_sim	      ( interictal_sim )
	);


	integer i,i2,i3,check;;
	initial begin
		
		data_file = $fopen("/users/students/r0808764/thesis_project/hammer/e2e/src/skel4/tb/LBP_2.txt", "r");
                //data_file = $fopen("LBP_2.txt", "r");
  		if (data_file == `NULL) begin
    			$display("data_file handle was NULL");
    			$finish;
  		end

		
		clk = 1'b0;
		arst_n_in = 1'b0;
		use_mem = 0;
		write_mem = 0;
		
		// Wait for a clock edge
		@(posedge clk);


    		$fsdbDumpfile("output.fsdb");
    		$fsdbDumpvars("+all");
    		$fsdbDumpon;

		// Release the reset
		arst_n_in = 1'b1;


		scan_file = $fscanf(data_file, "%d\n", LBP_codes[0]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[1]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[2]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[3]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[4]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[5]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[6]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[7]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[8]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[9]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[10]);
		$display("LBP_codes0 = %d", LBP_codes[0]);
		$display("LBP_codes1 = %d", LBP_codes[1]);
		$display("LBP_codes2 = %d", LBP_codes[2]);
		$display("LBP_codes3 = %d", LBP_codes[3]);
		$display("LBP_codes4 = %d", LBP_codes[4]);
		$display("LBP_codes5 = %d", LBP_codes[5]);
		$display("LBP_codes6 = %d", LBP_codes[6]);
		$display("LBP_codes7 = %d", LBP_codes[7]);
		$display("LBP_codes8 = %d", LBP_codes[8]);
		$display("LBP_codes9 = %d", LBP_codes[9]);
		$display("LBP_codes10 = %d", LBP_codes[10]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[11]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[12]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[13]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[14]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[15]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[16]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[17]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[18]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[19]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[20]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[21]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[22]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[23]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[24]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[25]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[26]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[27]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[28]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[29]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[30]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[31]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[32]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[33]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[34]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[35]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[36]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[37]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[38]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[39]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[40]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[41]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[42]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[43]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[44]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[45]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[46]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[47]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[48]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[49]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[50]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[51]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[52]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[53]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[54]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[55]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[56]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[57]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[58]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[59]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[60]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[61]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[62]);
		scan_file = $fscanf(data_file, "%d\n", LBP_codes[63]);

		@(posedge clk);
		
		for (i=0;i<256*1*vector_fold_factor*channel_fold_factor+3;i=i+1) begin
			if (send_next_LBP == 1) begin
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[0]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[1]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[2]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[3]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[4]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[5]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[6]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[7]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[8]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[9]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[10]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[11]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[12]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[13]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[14]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[15]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[16]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[17]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[18]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[19]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[20]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[21]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[22]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[23]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[24]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[25]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[26]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[27]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[28]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[29]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[30]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[31]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[32]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[33]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[34]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[35]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[36]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[37]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[38]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[39]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[40]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[41]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[42]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[43]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[44]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[45]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[46]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[47]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[48]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[49]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[50]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[51]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[52]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[53]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[54]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[55]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[56]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[57]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[58]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[59]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[60]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[61]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[62]);
			scan_file = $fscanf(data_file, "%d\n", LBP_codes[63]);
			end
			else begin
			end

			if (classification_ready == 1) begin
				$display("Ictal sim = %d", ictal_sim);
				$display("Interictal sim = %d", interictal_sim);
			end
			@(posedge clk);
		end
		@(posedge clk);
		$display("***TEST COMPLETE***");
    		$fsdbDumpoff;
    		$finish;
	end




endmodule
